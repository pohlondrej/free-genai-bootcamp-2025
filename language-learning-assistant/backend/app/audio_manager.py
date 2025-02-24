from pathlib import Path
from typing import Optional
import os
from .config import settings

class AudioManager:
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir or settings.AUDIO_CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_audio_path(self, cache_key: str) -> Optional[Path]:
        """Get the full path for a cached audio file"""
        file_path = self.cache_dir / cache_key
        return file_path if file_path.exists() else None
    
    def save_audio(self, audio_data: bytes, cache_key: str) -> str:
        """Save audio data and return cache key"""
        file_path = self.cache_dir / cache_key
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        return cache_key