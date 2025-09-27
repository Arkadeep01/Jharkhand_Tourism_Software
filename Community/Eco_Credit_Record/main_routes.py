# main_routes.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from .models.eco_transaction import EcoTransactionIn, EcoTransactionOut
from .models.redemption import RedemptionIn, RedemptionOut
from . import db
from .services.credit_engine import assign_credits
from .services.redemption_engine import redeem_credits

router = APIRouter()

@router.post("/transactions", response_model=EcoTransactionOut, status_code=status.HTTP_201_CREATED)
def add_transaction(payload: EcoTransactionIn):
    try:
        saved = assign_credits(payload.dict(), db.transactions)
        # convert timestamp to ISO format string already stored
        return EcoTransactionOut(
            user_id=saved["user_id"],
            action=saved["action"],
            eco_score=saved["eco_score"],
            credits_earned=saved["credits_earned"],
            credits_balance=saved["credits_balance"],
            timestamp=saved["timestamp"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/redeem", response_model=RedemptionOut)
def redeem(payload: RedemptionIn):
    try:
        result = redeem_credits(payload.dict(), db.transactions, db.redemptions)
        redemption_doc = result["redemption"]
        return RedemptionOut(
            user_id=redemption_doc["user_id"],
            credits_used=redemption_doc["credits_used"],
            reward_item=redemption_doc["reward_item"],
            timestamp=redemption_doc["timestamp"],
            remaining_balance=result["remaining_balance"],
            redemption_id=str(redemption_doc["_id"])
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/balance/{user_id}")
def check_balance(user_id: str):
    last_tx = db.transactions.find_one({"user_id": user_id}, sort=[("_id", -1)])
    balance = int(last_tx["credits_balance"]) if last_tx and "credits_balance" in last_tx else 0
    return {"user_id": user_id, "balance": balance}

@router.get("/history/{user_id}", response_model=List[EcoTransactionOut])
def get_history(user_id: str, limit: int = 50):
    cursor = db.transactions.find({"user_id": user_id}).sort("_id", -1).limit(limit)
    out = []
    for d in cursor:
        out.append(EcoTransactionOut(
            user_id=d["user_id"],
            action=d["action"],
            eco_score=int(d.get("eco_score", 0)),
            credits_earned=int(d.get("credits_earned", 0)),
            credits_balance=int(d.get("credits_balance", 0)),
            timestamp=d["timestamp"]
        ))
    return out
