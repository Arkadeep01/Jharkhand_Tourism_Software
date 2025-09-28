from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "Fraud_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
fraud_results = db["fraud_results"]
fraud_aggregates = db["fraud_aggregates"]
