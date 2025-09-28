from sqlalchemy.orm import Session
from Profile_Section.models.eco_transaction import EcoTransaction
from Profile_Section.schemas.eco_transaction import EcoTransactionCreate
from datetime import datetime

def create_eco_transaction(db: Session, tx: EcoTransactionCreate):
    db_tx = EcoTransaction(
        user_id=tx.user_id,
        action_type=tx.action_type,
        points=tx.points,
        metadata=tx.metadata,
        created_at=datetime.utcnow()
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_eco_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(EcoTransaction).filter(EcoTransaction.user_id == user_id).offset(skip).limit(limit).all()

def get_eco_transaction(db: Session, tx_id: int):
    return db.query(EcoTransaction).filter(EcoTransaction.id == tx_id).first()
