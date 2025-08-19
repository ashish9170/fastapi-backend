from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.database import SessionLocal
#
# def get_user_by_email(email: str, db: Session = SessionLocal()):
#     return db.query(User).filter(User.email == email).first()
#
# def create_user(name: str, email: str, hashed_password: str, db: Session = SessionLocal()):
#     user = User(name=name, email=email, hashed_password=hashed_password)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
