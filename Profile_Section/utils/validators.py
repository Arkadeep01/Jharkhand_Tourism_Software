# Purpose of the file: Utility functions for validating inputs and getting current time in ISO format   

from datetime import datetime

def ensure_positive_int(value, name="value"):
    try:
        iv = int(value)
    except Exception:
        raise ValueError(f"{name} must be an integer")
    if iv < 0:
        raise ValueError(f"{name} must be >= 0")
    return iv

def now_iso():
    return datetime.utcnow().isoformat()