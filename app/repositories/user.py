# repositoris/user.py
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def create_user(user_data: UserCreate, hashed_password: str, db: Session):
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
