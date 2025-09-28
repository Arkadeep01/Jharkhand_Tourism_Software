from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EcoActionCreate(BaseModel):
    action_type: str
    points: int
    metadata: Optional[dict] = {}

class EcoActionRead(EcoActionCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
