import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client.get_database("eco_rewards")

# Collections
eco_transactions = db.get_collection("transactions")
eco_redemptions = db.get_collection("redemptions")
