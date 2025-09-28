from pydantic import BaseModel
from typing import Optional

class MitigationCreateSchema(BaseModel):
    title: str
    description: str
    risk_level: str
    user_id: int

class MitigationUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    risk_level: Optional[str]

class MitigationResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    risk_level: str
    user_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
