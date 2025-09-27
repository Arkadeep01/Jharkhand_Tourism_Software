# db.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise SystemExit("MONGO_URI not set in .env")

client = MongoClient(MONGO_URI)
db = client["jharkhand_tourism"]

transactions_col = db["transactions"]
wallets_col = db["wallets"]
