"""Dependencies for the onboarding module."""
from typing import Protocol, Optional, Dict, Any, Callable
from sqlalchemy.ext.asyncio import AsyncSession

class SettingsStore(Protocol):
    """Protocol for storing and retrieving settings."""
    @classmethod
    async def get_setting(cls, db: AsyncSession, key: str) -> Optional[str]:
        """Get a setting by key."""
        ...
    
    @classmethod
    async def set_setting(cls, db: AsyncSession, key: str, value: str) -> None:
        """Set a setting value."""
        ...
    
    @classmethod
    async def delete_setting(cls, db: AsyncSession, key: str) -> None:
        """Delete a setting by key."""
        ...

class WanikaniImporter(Protocol):
    """Protocol for importing data from Wanikani."""
    @classmethod
    def import_vocabulary(
        cls,
        api_key: str,
        output_dir: str,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> Dict[str, Any]:
        """Import vocabulary and kanji from Wanikani.
        
        Args:
            api_key: Wanikani API key
            output_dir: Directory to write migration file to
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with import statistics
        """
        ...
