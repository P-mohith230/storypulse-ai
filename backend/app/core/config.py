import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "StoryPulse AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["*"]

    # Database
    DATABASE_URL: str = "sqlite:///./storypulse.db"

    # Gnani AI Audio Platform
    GNANI_API_KEY: str = os.getenv("GNANI_API_KEY", "")
    GNANI_BASE_URL: str = "https://api.vachana.ai"
    GNANI_PRISMA_ENDPOINT: str = "/stt/v3"
    GNANI_TIMBRE_ENDPOINT: str = "/api/v1/tts/inference"
    GNANI_MOCK_FALLBACK: bool = True

    # LLM Settings
    LLM_PROVIDER: str = "mock_fallback"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
