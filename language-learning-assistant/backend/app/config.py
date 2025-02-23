import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", GEMINI_API_KEY)
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.9"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "30"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))
    LLM_TOP_P: float = float(os.getenv("LLM_TOP_P", "0.9"))
    LLM_FREQUENCY_PENALTY: float = float(os.getenv("LLM_FREQUENCY_PENALTY", "0.5"))
    LLM_STOP_SEQUENCES: Optional[list] = None
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "chroma_db")
    EMBEDDING_MODEL_API_KEY: str = os.getenv("EMBEDDING_MODEL_API_KEY", GEMINI_API_KEY)
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "gemini/text-embedding-004")

settings = Settings()
