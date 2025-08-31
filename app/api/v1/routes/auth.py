# app/api/v1/routes/auth.py

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import SignupRequest, LoginRequest, TokenResponse, TwoFAVerifySchema
from app.services.auth import signup_user, login_user
from app.services.twofa_service import verify_otp
from app.core.security import create_access_token
from app.repositories.user import get_user_by_email
from app.services.email_service import send_2fa_email

router = APIRouter()

@router.post("/signup")
def signup(
    data: SignupRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return signup_user(
        data,
        db,
        schedule_email_task=lambda email, code: background_tasks.add_task(send_2fa_email, email, code)
    )

@router.post("/login")
def login(
    data: LoginRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    return login_user(data, db, background_tasks)

@router.post("/verify-2fa", response_model=TokenResponse)
def verify_2fa(data: TwoFAVerifySchema, db: Session = Depends(get_db)):
    if not verify_otp(data.email, data.code):
        raise HTTPException(status_code=401, detail="Invalid or expired code")

    user = get_user_by_email(data.email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)
