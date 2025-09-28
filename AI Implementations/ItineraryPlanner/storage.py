"""
Simple JSON-based storage for generated itineraries and user history.
This avoids requiring a DB during prototyping; replace with SQL/NoSQL later if needed.
"""
import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path("data/itinerary")
SAVED_FILE = DATA_DIR / "saved_itineraries.json"

def _ensure_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SAVED_FILE.exists():
        with open(SAVED_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_itinerary(user_id: str, itinerary: Dict[str, Any]) -> None:
    """
    Append itinerary for a user. itinerary should include created_at, days, poi_ids.
    """
    _ensure_file()
    with open(SAVED_FILE, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append({"user_id": str(user_id), "itinerary": itinerary})
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()

def load_user_itineraries(user_id: str) -> List[Dict]:
    _ensure_file()
    with open(SAVED_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    return [entry["itinerary"] for entry in data if str(entry.get("user_id")) == str(user_id)]

def get_user_visited_pois(user_id: str) -> List[str]:
    """
    Read saved itineraries and return set of visited poi_ids.
    """
    itins = load_user_itineraries(user_id)
    visited = []
    for it in itins:
        for day in it.get("days", []):
            for item in day.get("items", []):
                pid = item.get("poi_id")
                if pid:
                    visited.append(pid)
    # return unique list
    return list(dict.fromkeys(visited))
