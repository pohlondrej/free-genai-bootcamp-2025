import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", GEMINI_API_KEY)
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "30"))

settings = Settings()
