# aggregator.py
from utils.db import visits_col, aggregates_col
from datetime import datetime, timedelta
import pandas as pd

def compute_daily(date_str):
    cursor = visits_col.find({"date": date_str})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        return None

    total_visits = len(df)
    avg_duration = float(df["duration_days"].mean())
    avg_spending = float(df["spending_usd"].mean())
    by_origin = df.groupby("origin_country").size().to_dict()
    by_age = df.groupby("age_group").size().to_dict()
    by_region = df.groupby("region_visited").size().to_dict()
    created_at = datetime.utcnow().isoformat()

    doc = {
        "date": date_str,
        "total_visits": total_visits,
        "avg_duration_days": avg_duration,
        "avg_spending_usd": avg_spending,
        "by_origin_country": by_origin,
        "by_age_group": by_age,
        "by_region": by_region,
        "created_at": created_at
    }
    aggregates_col.update_one({"date": date_str}, {"$set": doc}, upsert=True)
    return doc

if __name__ == "__main__":
    dt = datetime.utcnow().date() - timedelta(days=1)
    compute_daily(dt.isoformat())
