from db.connection import fraud_results, fraud_aggregates
from datetime import datetime

def aggregate_daily_anomalies():
    today = datetime.utcnow().date()
    pipeline = [
        {"$match": {"scored_at": {"$gte": datetime(today.year, today.month, today.day)}}},
        {"$group": {
            "_id": {"day": {"$substr": ["$scored_at", 0, 10]}},
            "count": {"$sum": 1},
            "avg_score": {"$avg": "$anomaly_score"}
        }}
    ]
    daily_stats = list(fraud_results.aggregate(pipeline))
    if daily_stats:
        fraud_aggregates.insert_many(daily_stats)
