from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class AppearanceBase(BaseModel):
    theme: Optional[str] = "light"
    palette_choice: Optional[str] = "default"
    font_family: Optional[str] = "Noto Sans"
    extra_settings: Optional[Dict] = {}

class AppearanceCreate(AppearanceBase):
    pass

class AppearanceUpdate(AppearanceBase):
    pass

class AppearanceRead(AppearanceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
