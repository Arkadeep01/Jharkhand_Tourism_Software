from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoticeBase(BaseModel):
    title: str
    message: str
    is_active: Optional[bool] = True

class NoticeCreate(NoticeBase):
    pass

class NoticeRead(NoticeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
