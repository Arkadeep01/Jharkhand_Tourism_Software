# scorer.py
import joblib
import json
import time
import os
from utils.db import r, STREAM_KEY, results_col, alerts_col, tx_col
from web3 import Web3
from datetime import datetime
from bson.objectid import ObjectId

MODEL_PATH = "model/isolation_forest_v1.joblib"
THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "0.7"))  # example: higher => more strict

def load_model():
    data = joblib.load(MODEL_PATH)
    return data["model"], data["feature_columns"]

def extract_features(tx_doc, feature_columns):
    """
    Map fields to numeric vector in same order as feature_columns.
    Example columns: ['amount','transaction_velocity_1h','avg_amount_7d','is_foreign_transaction_flag']
    """
    # This must match training preprocessing
    mapping = {
        "amount": float(tx_doc.get("amount", 0.0)),
        "transaction_velocity_1h": float(tx_doc.get("transaction_velocity_1h", 0)),
        "avg_amount_7d": float(tx_doc.get("avg_amount_7d", 0.0)),
        "is_foreign_transaction_flag": 1.0 if tx_doc.get("is_foreign_transaction") else 0.0
    }
    return [mapping.get(c, 0.0) for c in feature_columns]

def score_and_store(tx_doc, model, feature_columns):
    vec = extract_features(tx_doc, feature_columns)
    score = model.decision_function([vec])[0]  # higher -> more normal, negative = anomaly depending on scikit-learn
    # convert to normalized anomaly score 0..1
    # for IsolationForest, lower decision_function suggests anomaly; we can invert and scale
    anomaly_score = float(1.0 / (1.0 + abs(score)))  # simple transform (tune in prod)
    is_fraud = anomaly_score > THRESHOLD

    res = {
        "transaction_id": tx_doc["transaction_id"],
        "anomaly_score": anomaly_score,
        "is_fraud": is_fraud,
        "scored_at": datetime.utcnow().isoformat(),
        "model_version": "v1.0",
        "features": vec
    }
    results_col.insert_one(res)
    if is_fraud:
        alerts_col.insert_one({
            "transaction_id": tx_doc["transaction_id"],
            "user_id": tx_doc.get("user_id"),
            "anomaly_score": anomaly_score,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open"
        })
        # trigger external webhook / slack / email (omitted code - call alerts.send_alert)
    return res

def run_consumer():
    model, feature_columns = load_model()
    # read stream
    last_id = "0-0"
    while True:
        try:
            resp = r.xread({STREAM_KEY: last_id}, count=10, block=5000)
            if not resp:
                continue
            for stream, messages in resp:
                for msg_id, fields in messages:
                    last_id = msg_id
                    tx_json = fields.get(b"transaction") or fields.get("transaction")
                    if isinstance(tx_json, bytes):
                        tx_json = tx_json.decode()
                    tx_doc = json.loads(tx_json)
                    score = score_and_store(tx_doc, model, feature_columns)
                    print("Scored", tx_doc["transaction_id"], score["anomaly_score"])
        except Exception as e:
            print("Error in consumer:", e)
            time.sleep(2)

if __name__ == "__main__":
    run_consumer()
