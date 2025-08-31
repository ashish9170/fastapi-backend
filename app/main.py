from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.base import Base
from app.db.database import engine
from app.core.config import settings
from app.core.init_cors import init_cors

# Create tables if not existing (Alembic is better in prod though)
Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Middlewares
    init_cors(app)

    # Routers
    app.include_router(api_router)

    # Health check / root
    @app.get("/")
    def root():
        return {"message": f"Welcome to {settings.PROJECT_NAME}", "env": settings.ENV}

    return app

app = create_app()
