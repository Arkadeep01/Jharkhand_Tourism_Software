# upload_certificates.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["NFT_CERTIFICATES"]
certificates_col = db["certificates_col"]

# Sample certificate data
sample_cert = {
    "cert_id": "CERT001",
    "person_name": "Ramesh Kumar",
    "role": "Tour Guide",
    "nft_id": "",  # will fill after minting
    "wallet_address": "0xRecipientWalletAddressHere",
    "issue_date": datetime.utcnow().isoformat()
}

certificates_col.insert_one(sample_cert)
print("Sample certificate uploaded:", sample_cert)
