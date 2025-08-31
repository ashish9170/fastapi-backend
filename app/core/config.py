from pydantic_settings import BaseSettings
from typing import List, Optional
import os, redis
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"

    # Database URLs
    DATABASE_URL: Optional[str] = None
    DATABASE_PUBLIC_URL: Optional[str] = None

    SECRET_KEY: str
    ANOTHER_VAR: Optional[str] = None
    EMAIL_PROVIDER: str
    BRAVO_API_KEY: str
    BRAVO_API_URL: str
    ENV: str = Field(default="local", alias="APP_ENV")

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    BACKEND_CORS_ORIGINS: List[str] = []

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.configure_env()

    def configure_env(self):
        # Select correct DATABASE_URL based on ENV
        if self.ENV == "local":
            # Use the loaded value, not os.getenv()
            if self.DATABASE_PUBLIC_URL:
                self.DATABASE_URL = self.DATABASE_PUBLIC_URL
        else:
            # For non-local environments, DATABASE_URL should already be set
            pass

        # Configure CORS
        if self.ENV == "local":
            self.BACKEND_CORS_ORIGINS = [
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ]
        elif self.ENV == "staging":
            self.BACKEND_CORS_ORIGINS = ["https://staging.myfrontend.com"]
        elif self.ENV == "prod":
            self.BACKEND_CORS_ORIGINS = ["https://myfrontend.com"]

    @property
    def redis_client(self):
        return redis.StrictRedis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
            decode_responses=True
        )


# Create settings object
settings = Settings()