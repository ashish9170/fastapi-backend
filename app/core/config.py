from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:password@localhost:5432/abhinav"

    class Config:
        env_file = ".env"

settings = Settings()
