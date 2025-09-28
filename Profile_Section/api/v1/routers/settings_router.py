from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Profile_Section.db.session import get_db
from Profile_Section.crud import user as crud_user
from Profile_Section.utils.response import success_response, error_response

router = APIRouter(prefix="/settings", tags=["settings"])

@router.put("/{user_id}")
def update_settings(user_id: int, settings: dict, db: Session = Depends(get_db)):
    try:
        updated = crud_user.update_settings(db, user_id, settings)
        return success_response(updated, message="Settings updated")
    except Exception as e:
        return error_response("Failed to update settings", details=str(e))
