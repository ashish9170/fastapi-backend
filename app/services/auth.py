# app/services/auth.py

from fastapi import HTTPException, status, BackgroundTasks
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user import get_user_by_email, create_user
from app.services.twofa_service import generate_otp, save_otp
from app.services.email_service import send_2fa_email
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# app/services/auth.py

def signup_user(data: SignupRequest, db: Session, schedule_email_task: callable):
    if get_user_by_email(data.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(data.password)
    user = create_user(
        UserCreate(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            email=data.email,
            password=data.password
        ),
        hashed_pw,
        db
    )

    code = generate_otp()
    save_otp(user.email, code)
    schedule_email_task(user.email, code)
    token = create_access_token(
        {"sub": user.email, "scope": "2fa_pending"},
        expires_delta=timedelta(seconds=300)
    )
    return {"message": "Signup successful. Check your email for the 2FA code.", "pre_auth_token": token}


def login_user(data: LoginRequest, db: Session, background_tasks: BackgroundTasks):
    user = get_user_by_email(data.email, db)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    code = generate_otp()
    save_otp(user.email, code)
    background_tasks.add_task(send_2fa_email, user.email, code)

    pre_auth_token = create_access_token(
        {"sub": user.email, "scope": "2fa_pending"}, expires_delta=300
    )

    return {"message": "Login successful. Check your email for the 2FA code.", "pre_auth_token": pre_auth_token}
