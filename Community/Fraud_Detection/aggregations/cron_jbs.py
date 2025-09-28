from apscheduler.schedulers.blocking import BlockingScheduler
from aggregations import daily_aggregation, user_risk

def schedule_jobs():
    scheduler = BlockingScheduler()

    # Daily anomaly aggregation at 00:05 UTC
    scheduler.add_job(daily_aggregation.aggregate_daily_anomalies, 'cron', hour=0, minute=5)

    # User risk score every hour
    scheduler.add_job(user_risk.compute_user_risk, 'interval', hours=1)

    print("Scheduler started. Running jobs...")
    scheduler.start()

if __name__ == "__main__":
    schedule_jobs()
