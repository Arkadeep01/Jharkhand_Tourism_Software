from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from Profile_Section.schemas.auth import LoginData
from Profile_Section.utils.response import success_response, error_response
from Profile_Section.Core.firebase_admin_init import firebase_app
from firebase_admin import auth as firebase_auth

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(data: LoginData):
    try:
        # Verify Firebase ID token instead of traditional login
        decoded_token = firebase_auth.verify_id_token(data.password)
        return success_response({"user": decoded_token})
    except Exception as e:
        return error_response("Invalid credentials", details=str(e))
