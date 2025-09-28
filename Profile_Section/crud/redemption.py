from sqlalchemy.orm import Session
from Profile_Section.models.redemption import Redemption
from Profile_Section.schemas.redemption import RedemptionCreate
from datetime import datetime

def create_redemption(db: Session, redemption: RedemptionCreate):
    db_red = Redemption(
        user_id=redemption.user_id,
        item_name=redemption.item_name,
        points_used=redemption.points_used,
        metadata=redemption.metadata,
        created_at=datetime.utcnow()
    )
    db.add(db_red)
    db.commit()
    db.refresh(db_red)
    return db_red

def get_redemptions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Redemption).filter(Redemption.user_id == user_id).offset(skip).limit(limit).all()

def get_redemption(db: Session, redemption_id: int):
    return db.query(Redemption).filter(Redemption.id == redemption_id).first()
