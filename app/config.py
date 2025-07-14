from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 👇 Load the .env file from the correct path
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

class Settings(BaseSettings):
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # Not required with load_dotenv but still good

settings = Settings()