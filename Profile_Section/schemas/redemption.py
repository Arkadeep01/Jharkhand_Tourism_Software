from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class RedemptionBase(BaseModel):
    user_id: int
    item_name: str
    points_used: int
    metadata: Optional[Dict] = {}

class RedemptionCreate(RedemptionBase):
    pass

class RedemptionRead(RedemptionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
