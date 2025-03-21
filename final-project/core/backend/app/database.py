from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Database configuration
DB_DIR = "/app/data/db"
DB_FILE = "waniduokani.db"
DB_PATH = os.path.join(DB_DIR, DB_FILE)
DATABASE_URL = f"sqlite:///{DB_PATH}"
ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

async def init_db():
    """Initialize database directory and check access"""
    try:
        # Ensure database directory exists
        Path(DB_DIR).mkdir(parents=True, exist_ok=True)
        
        # Check if we can write to the directory
        test_file = os.path.join(DB_DIR, ".write_test")
        try:
            Path(test_file).touch()
            os.remove(test_file)
            logger.info(f"Database directory {DB_DIR} is writable")
        except OSError as e:
            logger.error(f"Database directory {DB_DIR} is not writable: {e}")
            raise

        # Initialize engine
        engine = create_async_engine(
            ASYNC_DATABASE_URL,
            echo=True  # Set to False in production
        )
        
        return engine
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def get_db():
    """Get database session"""
    try:
        engine = await init_db()
        async_session = sessionmaker(
            engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        async with async_session() as session:
            yield session
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
