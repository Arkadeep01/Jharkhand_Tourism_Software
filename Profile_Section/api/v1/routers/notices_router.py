from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Profile_Section.db.session import get_db
from Profile_Section.crud import notice as crud_notice
from Profile_Section.schemas.notice import NoticeCreate, NoticeRead
from Profile_Section.utils.response import success_response, error_response

router = APIRouter(prefix="/notices", tags=["notices"])

@router.get("/")
def get_notices(db: Session = Depends(get_db)):
    notices = crud_notice.get_all_notices(db)
    return success_response(notices)

@router.post("/")
def create_notice(data: NoticeCreate, db: Session = Depends(get_db)):
    try:
        notice = crud_notice.create_notice(db, data)
        return success_response(notice)
    except Exception as e:
        return error_response("Failed to create notice", details=str(e))
