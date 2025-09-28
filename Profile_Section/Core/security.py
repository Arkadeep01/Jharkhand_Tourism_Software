from fastapi import HTTPException, Depends, Request
from firebase_admin import auth as firebase_auth
from Profile_Section.db.session import get_db
from sqlalchemy.orm import Session
from Profile_Section import crud

def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Verify Firebase ID token and return the user from local DB (optional: auto-create user)
    """
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.split(" ")[1]
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

    # Optional: fetch local user by email
    user = crud.user.get_user_by_email(db, email)
    
    # Optional: auto-create local user if not exists
    if not user:
        user_create = {
            "username": email.split("@")[0],
            "email": email,
            "first_name": decoded_token.get("name", ""),
            "last_name": "",
            "password": None,  # password not used with Firebase
        }
        user = crud.user.create_user_from_firebase(db, user_create)

    return user

def get_current_user(request: Request):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = authorization.split(" ")[1]  # Bearer <token>
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")