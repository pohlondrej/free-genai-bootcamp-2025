"""Onboarding router for handling application initialization."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Type
from .dependencies import SettingsStore

class InitializeRequest(BaseModel):
    api_key: str

class OnboardingResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    is_initialized: bool = False

def create_router(
    get_db,
    settings_store: Type[SettingsStore]
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
        db: AsyncSession = Depends(get_db)
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
            
            # TODO: Import data using wkimporter
            # from modules.wkimporter.main import import_from_wanikani
            # await import_from_wanikani(request.api_key)
            
            # Mark as initialized
            await settings_store.set_setting(db, "is_initialized", "true")
            
            return OnboardingResponse(
                success=True,
                is_initialized=True,
                message="Application initialized successfully"
            )
        except Exception as e:
            # Cleanup on failure
            await settings_store.set_setting(db, "wanikani_api_key", "")
            await settings_store.set_setting(db, "is_initialized", "false")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize: {str(e)}"
            )
    
    return router
