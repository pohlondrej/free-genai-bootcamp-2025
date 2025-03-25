"""Dependencies for the onboarding module."""
from typing import Protocol, Optional
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
