from sqlalchemy.orm import Session
from Profile_Section.models.announcement import Announcement
from Profile_Section.schemas.announcement import AnnouncementBase
from datetime import datetime

def create_announcement(db: Session, announcement: AnnouncementBase):
    db_announcement = Announcement(
        title=announcement.title,
        content=announcement.content,
        is_active=announcement.is_active,
        created_at=datetime.utcnow()
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def get_announcements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Announcement).offset(skip).limit(limit).all()

def get_announcement(db: Session, announcement_id: int):
    return db.query(Announcement).filter(Announcement.id == announcement_id).first()
