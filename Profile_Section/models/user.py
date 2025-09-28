from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from Profile_Section.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    phone = Column(String(20))
    bio = Column(Text)
    avatar_url = Column(String(1024))
    location = Column(String(255))
    traveler_type = Column(String(50))       # enum-like: solo, family, group, researcher
    interests = Column(JSON)                 # JSON array: ["wildlife","culture"]
    eco_score = Column(Integer, default=0)
    eco_badges = Column(JSON, default=[])    # list of badge ids or names
    settings = Column(JSON, default={})      # notification preferences, privacy
    appearance = Column(JSON, default={})    # theme, language, font size
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
