"""Onboarding router for handling application initialization."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Type
from .dependencies import SettingsStore, WanikaniImporter
import os
from pathlib import Path
from database import run_migrations

class InitializeRequest(BaseModel):
    api_key: str

class OnboardingResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    is_initialized: bool = False

def create_router(
    get_db,
    settings_store: Type[SettingsStore],
    wanikani_importer: Type[WanikaniImporter]
) -> APIRouter:
    """Create the onboarding router with injected dependencies."""
    router = APIRouter(
        prefix="/onboarding",
        tags=["onboarding"]
    )

    @router.get("/status")
    async def get_status(db: AsyncSession = Depends(get_db)) -> OnboardingResponse:
        """Check if the application has been initialized."""
        is_initialized = await settings_store.get_setting(db, "is_initialized")
        return OnboardingResponse(
            success=True,
            is_initialized=is_initialized == "true",
            message="initialized" if is_initialized == "true" else "not_initialized"
        )

    @router.post("/initialize")
    async def initialize(
        request: InitializeRequest,
        db: AsyncSession = Depends(get_db),
        importer: WanikaniImporter = Depends(wanikani_importer)
    ) -> OnboardingResponse:
        """Initialize the application with WaniKani API key."""
        # Check if already initialized
        is_initialized = await settings_store.get_setting(db, "is_initialized")
        if is_initialized == "true":
            raise HTTPException(
                status_code=400,
                detail="Application is already initialized"
            )
        
        try:
            # Store API key
            await settings_store.set_setting(db, "wanikani_api_key", request.api_key)
            
            # Import data from WaniKani
            migrations_dir = Path("/app/database")  # Docker path
            result = importer.import_vocabulary(
                api_key=request.api_key,
                output_dir=str(migrations_dir)
            )
            
            # Run migrations to import the data
            await run_migrations(db)
            
            # Clean up the migration file
            try:
                os.remove(result['output_file'])
            except Exception as e:
                # Log but don't fail if cleanup fails
                print(f"Warning: Failed to clean up migration file: {e}")
            
            # Mark as initialized
            await settings_store.set_setting(db, "is_initialized", "true")
            
            return OnboardingResponse(
                success=True,
                is_initialized=True,
                message=f"Application initialized successfully. Imported {result['kanji_count']} kanji and {result['vocab_count']} vocabulary items."
            )
        except Exception as e:
            # Cleanup on failure
            await settings_store.delete_setting(db, "wanikani_api_key")
            await settings_store.delete_setting(db, "is_initialized")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize application: {str(e)}"
            )

    return router
