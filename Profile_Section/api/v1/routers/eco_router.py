from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Profile_Section.db.session import get_db
from Profile_Section.schemas.eco_action import EcoActionCreate, EcoActionRead
from Profile_Section.crud import eco_action as crud_eco
from Profile_Section.utils.response import success_response, error_response

router = APIRouter(prefix="/eco", tags=["eco"])

@router.post("/log", response_model=EcoActionRead)
def log_eco_action(data: EcoActionCreate, db: Session = Depends(get_db)):
    try:
        action = crud_eco.create_eco_action(db, data)
        return success_response(action)
    except Exception as e:
        return error_response("Failed to log action", details=str(e))
