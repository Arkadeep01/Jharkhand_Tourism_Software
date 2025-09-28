import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ALERT_SERVICE_URL = os.getenv("ALERT_SERVICE_URL")

def send_slack_alert(message: str):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print(f"Slack alert failed: {response.text}")

def send_http_alert(data: dict):
    response = requests.post(ALERT_SERVICE_URL, json=data)
    if response.status_code != 200:
        print(f"HTTP alert failed: {response.text}")

# Example usage:
if __name__ == "__main__":
    alert_message = "Anomaly detected for user USR-1001"
    send_slack_alert(alert_message)
    send_http_alert({"user_id": "USR-1001", "anomaly_score": 0.95})
