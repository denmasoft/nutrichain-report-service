from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "NutriChain Reports"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "dev"

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    RATE_LIMIT_GUEST: str = "100/minute"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()