from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.base import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Project"}
