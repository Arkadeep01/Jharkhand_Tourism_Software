from pydantic import BaseModel, Field, constr
from typing import Optional, Annotated
from datetime import datetime

class EcoTransactionIn(BaseModel):
    user_id: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    action: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    eco_score: Optional[int] = None


class EcoTransactionOut(BaseModel):
    user_id: str
    action: str
    eco_score: int
    credits_earned: int
    credits_balance: int
    timestamp: datetime