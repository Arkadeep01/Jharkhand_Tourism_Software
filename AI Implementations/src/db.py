from pymongo import MongoClient
import certifi
import os
from datetime import datetime, timezone

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())

# Create/use database
db = client["chatbotDB"]

# Collections
users_col = db["users"]
conversations_col = db["conversations"]
faq_col = db["faq_responses"]
translations_col = db["translations"]