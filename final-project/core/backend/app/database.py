from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import logging
from pathlib import Path
from models import Base
from sqlalchemy import text

logger = logging.getLogger(__name__)

# Database configuration - path from docker volume mapping
DB_DIR = "/app/data/db"
DB_FILE = "duokani.db"
DB_PATH = os.path.join(DB_DIR, DB_FILE)
DATABASE_URL = f"sqlite:///{DB_PATH}"
ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Module level engine instance
engine = None

async def run_migrations(db):
    """Run SQL migration scripts"""
    try:
        # Get all .sql files from the database directory in sorted order
        migrations_dir = os.path.join(os.path.dirname(__file__), "database")
        migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
        
        for migration_file in migration_files:
            logger.info(f"Running migration: {migration_file}")
            with open(os.path.join(migrations_dir, migration_file)) as f:
                sql = f.read()
                # Split on semicolon to handle multiple statements
                statements = [s.strip() for s in sql.split(';') if s.strip()]
                for statement in statements:
                    if statement:  # Only execute non-empty statements
                        await db.execute(text(statement))
        await db.commit()
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")
        raise

async def init_db():
    """Initialize database directory and check access. Should only be called once on startup."""
    global engine
    
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

        # Initialize engine if not already created
        if engine is None:
            engine = create_async_engine(
                ASYNC_DATABASE_URL,
                echo=True  # Set to False in production
            )

            # Run migrations if database file doesn't exist or to ensure schema is up to date
            async with AsyncSession(engine) as session:
                await run_migrations(session)
                await session.commit()
        
        return engine
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def get_engine():
    """Get the SQLAlchemy engine instance, initializing it if necessary"""
    global engine
    if engine is None:
        engine = await init_db()
    return engine

async def get_db():
    """Get database session"""
    try:
        engine = await get_engine()
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
