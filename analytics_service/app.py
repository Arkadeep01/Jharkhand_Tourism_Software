# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .utils.db import visits_col, aggregates_col
from datetime import datetime
from typing import Optional, List

app = FastAPI(title="Jharkhand Tourism Analytics Service")

class VisitIn(BaseModel):
    visit_id: str
    date: str  # ISO YYYY-MM-DD
    origin_country: str
    age_group: str
    travel_type: str
    duration_days: int
    spending_usd: float
    region_visited: str
    satisfaction_score: Optional[int] = None

@app.post("/ingest/visit")
def ingest_visit(v: VisitIn):
    doc = v.dict()
    doc["ingested_at"] = datetime.utcnow().isoformat()
    visits_col.insert_one(doc)
    return {"ok": True, "visit_id": doc["visit_id"]}

@app.get("/aggregates/daily/{date}")
def get_daily_aggregate(date: str):
    agg = aggregates_col.find_one({"date": date})
    if not agg:
        raise HTTPException(status_code=404, detail="No aggregate for date")
    return agg

@app.get("/aggregates/daterange")
def get_range(start: str, end: str):
    cursor = aggregates_col.find({"date": {"$gte": start, "$lte": end}}).sort("date", 1)
    return list(cursor)
