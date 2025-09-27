from typing import Dict, Any
from datetime import datetime
from pymongo.collection import Collection
from ..utils.scoring import get_score
from ..utils.validators import now_iso

# The service functions expect to use the shared db collections from db.py
def assign_credits(txn_in: Dict[str, Any], transactions_col: Collection) -> Dict[str, Any]:
    """
    txn_in: { user_id, action, eco_score (optional) }
    returns the saved transaction document
    """
    user_id = txn_in["user_id"]
    action = txn_in["action"]
    eco_score = txn_in.get("eco_score")
    if eco_score is None:
        eco_score = get_score(action)

    # credits earned mapping (here 1:1 with eco_score; change multiplier if needed)
    credits_earned = int(eco_score)

    # compute previous balance
    last = transactions_col.find_one({"user_id": user_id}, sort=[("_id", -1)])
    prev_balance = int(last["credits_balance"]) if last and "credits_balance" in last else 0
    new_balance = prev_balance + credits_earned

    doc = {
        "user_id": user_id,
        "action": action,
        "eco_score": int(eco_score),
        "credits_earned": credits_earned,
        "credits_balance": new_balance,
        "timestamp": datetime.utcnow().isoformat()
    }

    result = transactions_col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc
