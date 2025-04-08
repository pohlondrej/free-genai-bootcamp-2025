from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plugin configuration
PLUGIN_ID = "flashcards"
PLUGIN_NAME = "Flashcards"
PLUGIN_DESCRIPTION = "Practice your Japanese vocabulary by studying flashcards."
PLUGIN_IMAGE = "./assets/flashcards.svg"
PLUGIN_PORT = 8002
PLUGIN_FRONTEND_PORT = 4202
MAIN_APP_URL = "http://nginx:80"
REGISTRATION_RETRY_DELAY = 5  # seconds
MAX_RETRIES = 30  # 5 seconds * 30 = 2.5 minutes max wait

app = FastAPI(
    title="Flashcard API",
    description="Flashcard Plugin API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    root_path="/api"
)

# Configure CORS - allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/image")
async def get_image():
    return FileResponse(PLUGIN_IMAGE)

async def register_plugin():
    """Register this plugin with the main application with retries"""
    plugin_data = {
        "id": PLUGIN_ID,
        "name": PLUGIN_NAME,
        "description": PLUGIN_DESCRIPTION,
        "backend_endpoint": f"http://localhost:{PLUGIN_PORT}",
        "frontend_endpoint": f"http://localhost:{PLUGIN_FRONTEND_PORT}",
        "module_name": PLUGIN_ID
    }
    
    retries = 0
    while retries < MAX_RETRIES:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{MAIN_APP_URL}/api/plugins/register",
                    json=plugin_data
                ) as response:
                    if response.status == 200:
                        logger.info("Plugin registered successfully")
                        return True
                    else:
                        text = await response.text()
                        logger.warning(f"Registration attempt {retries + 1} failed: {text}")
        except Exception as e:
            logger.warning(f"Registration attempt {retries + 1} failed: {e}")
        
        retries += 1
        logger.info(f"Retrying registration in {REGISTRATION_RETRY_DELAY} seconds...")
        await asyncio.sleep(REGISTRATION_RETRY_DELAY)
    
    logger.error("Failed to register plugin after maximum retries")
    return False

@app.on_event("startup")
async def startup_event():
    # First register the plugin with retries
    if not await register_plugin():
        logger.error(f"{PLUGIN_ID} registration failed, exiting...")
        exit(323)
