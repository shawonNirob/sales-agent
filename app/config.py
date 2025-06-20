from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    MODEL_ID: str
    S2_STRING: str

    class Config:
        env_file = ".env"

settings = Settings()

