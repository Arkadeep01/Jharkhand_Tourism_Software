from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from Profile_Section.db.base import Base

class EcoAction(Base):
    __tablename__ = "eco_actions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    action_type = Column(String(100))  # eco_stay, local_transport, etc.
    points = Column(Integer)
    metadata = Column(JSON)            # place, notes, receipts
    created_at = Column(DateTime(timezone=True), server_default=func.now())
