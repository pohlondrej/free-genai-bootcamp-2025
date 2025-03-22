from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from models import User
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DuoKani WaniLingo API",
    description="Japanese Language Learning Platform API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    root_path="/api"
)

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint that verifies API and database availability
    """
    try:
        # Test database connection with a simple model query
        await db.execute(text("SELECT COUNT(*) FROM user"))
        
        # Test configuration store
        test_key = "health_check"
        await User.set_setting(db, test_key, "ok")
        value = await User.get_setting(db, test_key)
        await db.execute(text("DELETE FROM user WHERE key = :key"), {"key": test_key})
        await db.commit()
        
        return {
            "status": "healthy",
            "database": "connected",
            "config_store": "working" if value == "ok" else "error"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
