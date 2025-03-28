from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db, init_db
from models import User
import logging
from routers import words, kanji, groups, study_activities
from onboarding import create_router
from wkimporter.main import import_vocabulary
from fastapi.middleware.cors import CORSMiddleware

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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Create WaniKani importer class that matches the protocol
class WanikaniImporter:
    @classmethod
    def import_vocabulary(cls, api_key, output_dir, progress_callback=None):
        return import_vocabulary(api_key, output_dir, progress_callback)

# Initialize onboarding module with dependencies
onboarding_router = create_router(get_db, User, WanikaniImporter)
app.include_router(onboarding_router)

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint that verifies API and database availability"""
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        
        # Check if application is initialized
        is_initialized = await User.get_setting(db, "is_initialized")
        
        return {
            "status": "healthy",
            "database": "connected",
            "initialized": is_initialized == "true"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
