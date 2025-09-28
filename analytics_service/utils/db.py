# utils/db.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["jharkhand_tourism"]

visits_col = db["tourism_visits"]
aggregates_col = db["tourism_aggregates"]
