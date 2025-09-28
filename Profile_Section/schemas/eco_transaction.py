from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class EcoTransactionBase(BaseModel):
    user_id: int
    action_type: str
    points: int
    metadata: Optional[Dict] = {}

class EcoTransactionCreate(EcoTransactionBase):
    pass

class EcoTransactionRead(EcoTransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
