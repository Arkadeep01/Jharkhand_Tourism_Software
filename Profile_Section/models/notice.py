from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from Profile_Section.db.base import Base

class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    body = Column(Text)
    severity = Column(String(20))  # info/warning/critical
    area = Column(String(255))     # optional: affected region
    created_at = Column(DateTime(timezone=True), server_default=func.now())
