from sqlalchemy.orm import Session
from app.repositories import user
from app.schemas.user import UserCreate

def create_user_service(db: Session, user: UserCreate):
    return user_repository.create_user(db, user)

def list_users_service(db: Session):
    return user_repository.get_users(db)
