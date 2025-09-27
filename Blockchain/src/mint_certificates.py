import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from web3 import Web3
from datetime import datetime

load_dotenv()

# Env variables
RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL")
PRIVATE_KEY = os.getenv("BACKEND_PRIVATE_KEY")
FROM_ADDRESS = os.getenv("BACKEND_ADDRESS")
NFT_CONTRACT_ADDRESS = os.getenv("NFT_CONTRACT_ADDRESS")
MONGO_URI = os.getenv("MONGO_URI")
CHAIN_ID = int(os.getenv("CHAIN_ID", "80001"))

# Mongo
client = MongoClient(MONGO_URI)
db = client["NFT_CERTIFICATES"]
cert_col = db["certificates_col"]

# Blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise SystemExit("Failed to connect to RPC")

# Minimal ABI for mintCertificate
NFT_ABI = [
    {
      "inputs": [
        {"internalType":"address","name":"recipient","type":"address"},
        {"internalType":"string","name":"certId","type":"string"},
        {"internalType":"string","name":"tokenURI","type":"string"}
      ],
      "name":"mintCertificate",
      "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
      "stateMutability":"nonpayable",
      "type":"function"
    },
    {
      "inputs":[{"internalType":"string","name":"certId","type":"string"}],
      "name":"getTokenId",
      "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
      "stateMutability":"view",
      "type":"function"
    }
]

contract = w3.eth.contract(address=Web3.to_checksum_address(NFT_CONTRACT_ADDRESS), abi=NFT_ABI)

def mint_certificate(cert_id, recipient_address, tokenURI):
    nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(FROM_ADDRESS))
    txn = contract.functions.mintCertificate(recipient_address, cert_id, tokenURI).build_transaction({
        "from": Web3.to_checksum_address(FROM_ADDRESS),
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei(2, "gwei"),
        "chainId": CHAIN_ID
    })

    signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
    token_id = contract.functions.getTokenId(cert_id).call()
    
    # Update MongoDB
    cert_col.update_one({"cert_id": cert_id}, {"$set": {"nft_id": token_id, "minted_at": datetime.utcnow().isoformat()}})
    
    return token_id, receipt.transactionHash.hex()

# Example usage
if __name__ == "__main__":
    cert = cert_col.find_one({"cert_id": "CERT001"})
    if cert:
        token_uri = "https://example.com/metadata/CERT001.json"  # URL for NFT metadata (JSON)
        token_id, tx_hash = mint_certificate(cert["cert_id"], cert["wallet_address"], token_uri)
        print(f"NFT minted! token_id={token_id}, tx_hash={tx_hash}")