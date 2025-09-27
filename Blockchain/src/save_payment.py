# save_payment.py
import os
import json
import hashlib
from dotenv import load_dotenv
from web3 import Web3
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

# ENV variables (set in .env)
RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL")            
PRIVATE_KEY = os.getenv("BACKEND_PRIVATE_KEY")        
FROM_ADDRESS = os.getenv("BACKEND_ADDRESS")           
CONTRACT_ADDRESS = os.getenv("PAYMENT_PROOF_CONTRACT")
MONGO_URI = os.getenv("MONGO_URI")
CHAIN_ID = int(os.getenv("CHAIN_ID", "80001"))        

if not (RPC_URL and PRIVATE_KEY and FROM_ADDRESS and CONTRACT_ADDRESS and MONGO_URI):
    raise SystemExit("Missing required environment variables. Check .env")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise SystemExit("Failed to connect to RPC")

CONTRACT_ABI = [
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "dataHash",
          "type": "string"
        }
      ],
      "name": "storeHash",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }
]

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["jharkhand_tourism"]
transactions_col = db["transactions"]


def compute_payment_hash(payment_obj: dict) -> str:
    tx_string = json.dumps(payment_obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(tx_string.encode("utf-8")).hexdigest()


def store_hash_on_chain(data_hash: str, gas_price_gwei: int = 2):
    nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(FROM_ADDRESS))
    txn = contract.functions.storeHash(data_hash).build_transaction({
        "from": Web3.to_checksum_address(FROM_ADDRESS),
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei(gas_price_gwei, "gwei"),
        "chainId": CHAIN_ID
    })
    signed = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
    return receipt


def record_payment(payment_payload: dict):
    # payment_payload sample keys: tx_id, user_id, amount, currency, payment_method, status, timestamp
    # 1) compute hash
    canonical = payment_payload.copy()
    # ensure timestamp exists
    canonical.setdefault("timestamp", datetime.utcnow().isoformat())
    canonical.setdefault("currency", "INR")

    data_hash = compute_payment_hash(canonical)

    # 2) write hash to chain and get receipt
    receipt = store_hash_on_chain(data_hash)

    blockchain_tx_hash = receipt.transactionHash.hex()
    block_number = receipt.blockNumber
    status = "confirmed" if receipt.status == 1 else "failed"

    # 3) save to MongoDB with blockchain proof fields
    doc = canonical.copy()
    doc.update({
        "blockchain_network": os.getenv("BLOCKCHAIN_NETWORK", "Polygon Mumbai"),
        "blockchain_tx_hash": blockchain_tx_hash,
        "data_hash": data_hash,
        "block_number": block_number,
        "onchain_status": status,
        "saved_at": datetime.utcnow().isoformat()
    })

    transactions_col.insert_one(doc)
    return doc