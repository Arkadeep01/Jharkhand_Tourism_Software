from typing import Dict, Any
from datetime import datetime
from pymongo.collection import Collection

def redeem_credits(redemption_in: Dict[str, Any], transactions_col: Collection, redemptions_col: Collection) -> Dict[str, Any]:
    """
    redemption_in: { user_id, credits_used, reward_item }
    Checks balance, creates a redemption record, and inserts a negative transaction to update balance.
    """
    user_id = redemption_in["user_id"]
    credits_used = int(redemption_in["credits_used"])
    reward_item = redemption_in["reward_item"]

    # fetch last balance
    last_tx = transactions_col.find_one({"user_id": user_id}, sort=[("_id", -1)])
    prev_balance = int(last_tx["credits_balance"]) if last_tx and "credits_balance" in last_tx else 0

    if credits_used > prev_balance:
        raise ValueError("Insufficient credits")

    new_balance = prev_balance - credits_used

    # redemption record
    redemption_doc = {
        "user_id": user_id,
        "credits_used": credits_used,
        "reward_item": reward_item,
        "timestamp": datetime.utcnow().isoformat()
    }
    r_res = redemptions_col.insert_one(redemption_doc)
    redemption_doc["_id"] = r_res.inserted_id

    # insert an entry in transactions as a negative credits entry for bookkeeping
    txn_doc = {
        "user_id": user_id,
        "action": f"Redeemed for: {reward_item}",
        "eco_score": 0,
        "credits_earned": 0,
        "credits_balance": new_balance,
        "timestamp": datetime.utcnow().isoformat()
    }
    t_res = transactions_col.insert_one(txn_doc)
    txn_doc["_id"] = t_res.inserted_id

    return {
        "redemption": redemption_doc,
        "transaction": txn_doc,
        "remaining_balance": new_balance
    }
