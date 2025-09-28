from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Profile_Section.db.session import get_db
from Profile_Section.crud import announcement as crud_ann
from Profile_Section.schemas.announcement import AnnouncementRead, AnnouncementCreate
from Profile_Section.utils.response import success_response, error_response

router = APIRouter(prefix="/announcements", tags=["announcements"])

@router.get("/")
def list_announcements(db: Session = Depends(get_db)):
    announcements = crud_ann.get_all_announcements(db)
    return success_response(announcements)

@router.post("/")
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db)):
    try:
        ann = crud_ann.create_announcement(db, data)
        return success_response(ann)
    except Exception as e:
        return error_response("Failed to create announcement", details=str(e))
