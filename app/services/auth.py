from app.schemas.auth import SignupRequest , LoginRequest , TokenResponse # or however you're handling signup
from app.schemas.user import UserCreate
from app.repositories.user import create_user, get_user_by_email
from app.core.security import hash_password, create_access_token, verify_password
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def signup_user(data: SignupRequest, db: Session):
    if get_user_by_email(data.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(data.password)
    user_data = UserCreate(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        email=data.email,
        password=data.password
    )

    user = create_user(user_data=user_data, hashed_password=hashed_pw, db=db)
    token = create_access_token({"sub": user.email})
    return {"access_token": token}


def login_user(data: LoginRequest):
    user = get_user_by_email(data.email)
    print(user , "++++++++++++++++++++++++++")
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)
