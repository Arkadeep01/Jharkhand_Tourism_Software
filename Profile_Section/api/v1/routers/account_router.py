from fastapi import APIRouter, Depends
from Profile_Section.utils.response import success_response
from Profile_Section.crud import user as crud_user
from Profile_Section.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/account", tags=["account"])

@router.get("/{user_id}")
def get_account(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_user(db, user_id)
    if not user:
        return {"error": "User not found"}
    return success_response(user)
