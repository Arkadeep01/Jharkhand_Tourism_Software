from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Profile_Section import db

app = FastAPI(title="Eco Credit API", version="1.0")

# Pydantic schemas
class TransactionSchema(BaseModel):
    user_id: str
    action: str

class RedeemSchema(BaseModel):
    user_id: str
    credits_used: int
    reward_item: str

@app.post("/api/v1/transactions")
async def add_transaction(payload: TransactionSchema):
    # calculate credits based on action
    action_credits = {
        "eco_hotel_stay": 50,
        "plant_tree": 30,
    }
    credits_earned = action_credits.get(payload.action, 10)

    # get previous balance
    last_tx = db.transactions.find_one({"user_id": payload.user_id}, sort=[("_id", -1)])
    balance = (last_tx.get("credits_balance") if last_tx else 0) + credits_earned

    # insert transaction
    tx_doc = {
        "user_id": payload.user_id,
        "action": payload.action,
        "credits_earned": credits_earned,
        "credits_balance": balance
    }
    inserted = db.transactions.insert_one(tx_doc)

    return {
        "user_id": payload.user_id,
        "credits_earned": credits_earned,
        "credits_balance": balance,
    }

@app.get("/api/v1/balance/{user_id}")
async def get_balance(user_id: str):
    last_tx = db.transactions.find_one({"user_id": user_id}, sort=[("_id", -1)])
    balance = last_tx.get("credits_balance") if last_tx else 0
    return {"balance": balance}

@app.post("/api/v1/redeem")
async def redeem_credits(payload: RedeemSchema):
    last_tx = db.transactions.find_one({"user_id": payload.user_id}, sort=[("_id", -1)])
    balance = last_tx.get("credits_balance") if last_tx else 0

    if balance < payload.credits_used:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    remaining_balance = balance - payload.credits_used

    db.redemptions.insert_one({
        "user_id": payload.user_id,
        "credits_used": payload.credits_used,
        "reward_item": payload.reward_item
    })

    # optionally, insert a negative transaction for tracking
    db.transactions.insert_one({
        "user_id": payload.user_id,
        "action": f"redeem_{payload.reward_item}",
        "credits_earned": -payload.credits_used,
        "credits_balance": remaining_balance
    })

    return {"remaining_balance": remaining_balance}
