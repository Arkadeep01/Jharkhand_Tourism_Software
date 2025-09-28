from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Profile_Section.db.session import get_db
from Profile_Section.crud import tourism as crud_tourism
from Profile_Section.utils.response import success_response, error_response

router = APIRouter(prefix="/tourism", tags=["tourism"])

@router.get("/places")
def list_places(db: Session = Depends(get_db)):
    places = crud_tourism.get_all_places(db)
    return success_response(places)
