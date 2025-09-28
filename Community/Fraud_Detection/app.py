# app.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
from .utils.db import tx_col, r, STREAM_KEY
import json

app = FastAPI(title="Fraud Ingest Service")

class TxIn(BaseModel):
    transaction_id: str
    user_id: str
    timestamp: str
    amount: float
    merchant_category: str
    location_city: str
    is_foreign_transaction: bool = False
    transaction_velocity_1h: int = 0
    avg_amount_7d: float = 0.0

@app.post("/ingest/transaction")
def ingest_tx(tx: TxIn, background_tasks: BackgroundTasks):
    doc = tx.dict()
    doc["raw_received_at"] = datetime.utcnow().isoformat()
    tx_col.insert_one(doc)
    # push to redis stream for scoring
    r.xadd(STREAM_KEY, {"transaction": json.dumps(doc)}, maxlen=10000)
    return {"ok": True, "transaction_id": doc["transaction_id"]}
