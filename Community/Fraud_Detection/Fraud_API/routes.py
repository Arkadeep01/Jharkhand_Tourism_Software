from fastapi import APIRouter
from db.connection import fraud_results

router = APIRouter()

@router.get("/transactions")
def get_transactions(limit: int = 10):
    return list(fraud_results.find().limit(limit))
