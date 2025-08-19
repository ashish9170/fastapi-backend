from fastapi import APIRouter
from app.api.v1.routes import user ,auth

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])


