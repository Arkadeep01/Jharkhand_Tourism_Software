from db.connection import fraud_results, fraud_aggregates
import pandas as pd
from datetime import datetime, timedelta

def compute_user_risk(window_hours: int = 24):
    """
    Compute rolling user risk score based on last `window_hours` of anomalies.
    """
    # Fetch recent transactions from MongoDB
    since_time = datetime.utcnow() - timedelta(hours=window_hours)
    cursor = fraud_results.find({"scored_at": {"$gte": since_time}})
    
    # Convert to DataFrame
    df = pd.DataFrame(list(cursor))
    if df.empty:
        print("No transactions found in the window.")
        return

    # Compute rolling average anomaly score per user
    df['scored_at'] = pd.to_datetime(df['scored_at'])
    df = df.sort_values(by=['user_id', 'scored_at'])
    
    user_scores = []
