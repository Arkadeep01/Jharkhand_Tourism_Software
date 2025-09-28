from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from Profile_Section.api.v1.routers import (
    eco_router,
    redeem_router,
    user_router,
    reward_router,
    profile_router,
    stats_router,
    leaderboard_router,
    notification_router,
    settings_router
)
from . import db
from .models.eco_transaction import EcoTransactionIn, EcoTransactionOut
from .models.redemption import RedemptionIn, RedemptionOut
from .services.credit_engine import assign_credits
from .services.redemption_engine import redeem_credits
from .helpers import success_response, error_response

router = APIRouter()

# --- Include external routers with prefixes and tags ---
router.include_router(eco_router.router, prefix="/eco", tags=["Eco Transactions"])
router.include_router(redeem_router.router, prefix="/redeem", tags=["Redemptions"])
router.include_router(user_router.router, prefix="/users", tags=["User Management"])
router.include_router(reward_router.router, prefix="/rewards", tags=["Rewards"])
router.include_router(profile_router.router, prefix="/profile", tags=["Profiles"])
router.include_router(stats_router.router, prefix="/stats", tags=["Statistics"])
router.include_router(leaderboard_router.router, prefix="/leaderboard", tags=["Leaderboard"])
router.include_router(notification_router.router, prefix="/notifications", tags=["Notifications"])
router.include_router(settings_router.router, prefix="/settings", tags=["Settings"])

# --- Transaction endpoints ---
@router.post("/transactions", response_model=EcoTransactionOut, status_code=status.HTTP_201_CREATED)
def add_transaction(payload: EcoTransactionIn):
    try:
        saved = assign_credits(payload.dict(), db.transactions)
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
    return success_response({"user_id": user_id, "balance": balance})

@router.get("/history/{user_id}", response_model=List[EcoTransactionOut])
def get_history(user_id: str, limit: int = 50):
    try:
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
        return success_response(out)
    except Exception as e:
        return error_response(str(e))