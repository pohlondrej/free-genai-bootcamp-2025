"""Onboarding router for handling application initialization."""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Type, Tuple
from .dependencies import SettingsStore, WanikaniImporter
from .websockets import manager
import os
from pathlib import Path
from database import run_migrations
import asyncio
from functools import partial
from queue import Queue

# Sentinel value to signal end of progress updates
PROGRESS_END = (None, None)

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

    @router.websocket("/progress")
    async def progress_endpoint(websocket: WebSocket):
        """WebSocket endpoint for progress updates."""
        await manager.connect(websocket)
        try:
            # Just keep the connection alive
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket)

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
            
            # Import data from WaniKani
            migrations_dir = Path("/app/database")  # Docker path
            
            # Create a queue for progress updates
            progress_queue: Queue[Tuple[Optional[str], Optional[float]]] = Queue()
            
            # Create a background task to process progress updates
            async def process_progress_updates():
                while True:
                    try:
                        message, percentage = progress_queue.get_nowait()
                        if (message, percentage) == PROGRESS_END:
                            break
                        await manager.broadcast({
                            "type": "import_progress",
                            "message": message,
                            "percentage": percentage
                        })
                    except:  # Queue empty
                        await asyncio.sleep(0.1)  # Short sleep to prevent CPU spin
            
            # Start progress processor task
            progress_task = asyncio.create_task(process_progress_updates())
            
            def progress_handler(message: str, percentage: float):
                """Handle progress updates by putting them in the queue."""
                progress_queue.put((message, percentage))
            
            # Run the import in a thread pool since it's CPU-bound
            loop = asyncio.get_event_loop()
            import_fn = partial(
                wanikani_importer.import_vocabulary,
                api_key=request.api_key,
                output_dir=str(migrations_dir),
                progress_callback=progress_handler
            )
            result = await loop.run_in_executor(None, import_fn)
            
            # Signal end of progress updates and wait for processor to finish
            progress_queue.put(PROGRESS_END)
            await progress_task
            
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
                message="Application initialized successfully",
                is_initialized=True
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize application: {str(e)}"
            )

    return router
