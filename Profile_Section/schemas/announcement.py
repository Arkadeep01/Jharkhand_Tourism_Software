from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnnouncementBase(BaseModel):
    title: str
    content: str
    is_active: Optional[bool] = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementRead(AnnouncementBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
