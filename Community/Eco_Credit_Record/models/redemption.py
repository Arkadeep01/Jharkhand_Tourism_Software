from pydantic import BaseModel, Field, constr
from typing import Optional, Annotated
from datetime import datetime

class EcoTransactionIn(BaseModel):
    user_id: Annotated[str, Field(strip_whitespace=True, min_length=1)]
    credits_used: Annotated[int, Field(gt=0)]
    reward_item: Annotated[str, Field(strip_whitespace=True, min_length=1)]

class RedemptionOut(BaseModel):
    user_id: str
    credits_used: int
    reward_item: str
    timestamp: datetime
    remaining_balance: int
    redemption_id: Optional[str] = None