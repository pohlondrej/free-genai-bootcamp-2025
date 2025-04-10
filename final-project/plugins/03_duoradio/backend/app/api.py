from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from quiz_manager import QuizManager
from models import QuizSession
from audio_manager import AudioManager
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plugin configuration
PLUGIN_ID = "duoradio"
PLUGIN_NAME = "DuoRadio"
PLUGIN_DESCRIPTION = "Practice listening with DuoRadio"
PLUGIN_IMAGE = "./assets/duoradio.svg"
PLUGIN_PORT = 8003
PLUGIN_FRONTEND_PORT = 4203
MAIN_APP_URL = "http://nginx:80"
REGISTRATION_RETRY_DELAY = 5  # seconds
MAX_RETRIES = 30  # 5 seconds * 30 = 2.5 minutes max wait

app = FastAPI(
    title="DuoRadio API",
    description="DuoRadio Plugin API",
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

# Gemini API key
gemini_api_key = None

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

async def get_gemini_api_key():
    """Fetch the Gemini API key from database."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{MAIN_APP_URL}/api/plugins/gemini_key",
                params={"plugin_id": PLUGIN_ID}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    global gemini_api_key
                    gemini_api_key = data
                    logger.info("Gemini API key fetched successfully: %s", gemini_api_key)
                else:
                    text = await response.text()
                    logger.warning(f"Failed to fetch Gemini API key: {text}")
                    return False
    except Exception as e:
        logger.warning(f"Failed to fetch Gemini API key: {e}")
        return False
    
    return True

@app.on_event("startup")
async def startup_event():
    # First register the plugin with retries
    if not await register_plugin():
        logger.error(f"{PLUGIN_ID} registration failed, exiting...")
        exit(323)

    # Get Gemini API key
    api_key = None
    if await get_gemini_api_key():
        api_key = gemini_api_key
    else:
        logger.warning("Gemini API key not found, defaulting to Ollama...")
    
    # Initialize LLM provider
    # TODO


quiz_manager = QuizManager()
audio_manager = AudioManager()

@app.post("/session/", response_model=QuizSession)
async def create_session():
    return await quiz_manager.create_session()

@app.get("/session/{session_id}", response_model=QuizSession)
async def get_session(session_id: UUID):
    session = quiz_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/session/{session_id}/answer")
async def submit_answer(session_id: UUID, answer: str):
    if not quiz_manager.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    correct = quiz_manager.submit_answer(session_id, answer)
    return {"correct": correct}

@app.get("/audio/{cache_key}")
async def get_audio(cache_key: str):
    """Stream audio file from cache"""
    audio_path = audio_manager.get_audio_path(cache_key)
    if not audio_path:
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        headers={"Accept-Ranges": "bytes"}
    )
