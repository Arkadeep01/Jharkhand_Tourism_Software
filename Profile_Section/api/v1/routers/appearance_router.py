from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Profile_Section.db.session import get_db
from Profile_Section.crud import appearance as crud_appearance
from Profile_Section.schemas.appearance import AppearanceRead, AppearanceUpdate
from Profile_Section.utils.response import success_response, error_response

router = APIRouter(prefix="/appearance", tags=["appearance"])

@router.get("/{user_id}", response_model=AppearanceRead)
def get_appearance(user_id: int, db: Session = Depends(get_db)):
    appearance = crud_appearance.get_appearance(db, user_id)
    if not appearance:
        return error_response("Appearance settings not found")
    return success_response(appearance)

@router.put("/{user_id}")
def update_appearance(user_id: int, data: AppearanceUpdate, db: Session = Depends(get_db)):
    try:
        updated = crud_appearance.update_appearance(db, user_id, data)
        return success_response(updated, message="Appearance updated")
    except Exception as e:
        return error_response("Failed to update appearance", details=str(e))
