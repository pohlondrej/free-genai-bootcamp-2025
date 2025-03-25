from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db, init_db
from models import User
import logging
from routers import words, kanji, groups, study_activities
from onboarding import create_router, SettingsStore

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

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()

# Include routers
app.include_router(words.router)
app.include_router(kanji.router)
app.include_router(groups.router)
app.include_router(study_activities.router)

# Initialize onboarding module
onboarding_router = create_router(get_db, User)
app.include_router(onboarding_router)

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint that verifies API and database availability
    """
    try:
        # Test database connection with a simple query
        await db.execute(text("SELECT COUNT(*) FROM user"))
        
        # Test configuration store
        test_key = "health_check"
        await db.execute(text("INSERT OR REPLACE INTO user (key, value) VALUES (:key, :value)"), 
                        {"key": test_key, "value": "ok"})
        result = await db.execute(text("SELECT value FROM user WHERE key = :key"), {"key": test_key})
        value = result.scalar()
        await db.execute(text("DELETE FROM user WHERE key = :key"), {"key": test_key})
        await db.commit()
        
        return {
            "status": "healthy",
            "database": "connected",
            "config_store": "working" if value == "ok" else "error"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
