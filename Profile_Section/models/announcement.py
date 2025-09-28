from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from Profile_Section.db.base import Base

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    body = Column(Text)
    posted_by = Column(Integer)         # admin user id
    start_at = Column(DateTime)
    end_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
