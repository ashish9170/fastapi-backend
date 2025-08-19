from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import SignupRequest , LoginRequest , TokenResponse
from app.services.auth import signup_user,login_user

router = APIRouter()

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    return signup_user(data, db)
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    return login_user(data)
