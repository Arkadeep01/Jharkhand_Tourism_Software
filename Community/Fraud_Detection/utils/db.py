# utils/db.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import redis

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

mongo = MongoClient(MONGO_URI)
db = mongo["jharkhand_tourism"]

tx_col = db["fraud_transactions"]
results_col = db["fraud_results"]
alerts_col = db["fraud_alerts"]
labeled_col = db["fraud_transactions_labeled"]

r = redis.from_url(REDIS_URL)
STREAM_KEY = "tx_stream"
