from sqlalchemy.orm import Session
from Profile_Section.models.notice import Notice
from Profile_Section.schemas.notice import NoticeBase
from datetime import datetime

def create_notice(db: Session, notice: NoticeBase):
    db_notice = Notice(
        title=notice.title,
        message=notice.message,
        is_active=notice.is_active,
        created_at=datetime.utcnow()
    )
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return db_notice

def get_notices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Notice).offset(skip).limit(limit).all()

def get_notice(db: Session, notice_id: int):
    return db.query(Notice).filter(Notice.id == notice_id).first()
