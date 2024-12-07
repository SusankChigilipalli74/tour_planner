from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    OPENAI_API_KEY: Optional[str] = None
    WEATHER_API_KEY: str
    NEWS_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()