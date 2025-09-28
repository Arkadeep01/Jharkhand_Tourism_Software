from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    traveler_type: Optional[str] = None
    interests: Optional[List[str]] = []

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    traveler_type: Optional[str]
    interests: Optional[List[str]]

class UserRead(UserBase):
    id: int
    eco_score: int
    eco_badges: List[str] = []
    settings: dict = {}
    appearance: dict = {}
    class Config:
        orm_mode = True
