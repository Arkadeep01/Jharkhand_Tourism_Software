from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from Profile_Section.db.base import Base


class EcoTransaction(Base):
    __tablename__ = "eco_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    action_type = Column(String(100), nullable=False)  # eco_stay, local_transport, etc.
    points = Column(Integer, nullable=False)
    metadata = Column(JSON, default={})                # place, notes, receipts

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
