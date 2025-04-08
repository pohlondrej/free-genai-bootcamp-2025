from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from typing import Dict, List, Optional
from fastapi.responses import FileResponse
import asyncio
import aiohttp
import logging
from agent import TopicExplorerAgent
from common.llms import LLMFactory
from common.llms.ollama import OllamaProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plugin configuration
PLUGIN_ID = "wkcrawler"
PLUGIN_NAME = "Wikipedia Crawler"
PLUGIN_DESCRIPTION = "Build your Japanese vocabulary by browsing Wikipedia articles."
PLUGIN_IMAGE = "./assets/wiki_crawler.svg"
PLUGIN_PORT = 8001
PLUGIN_FRONTEND_PORT = 4201
MAIN_APP_URL = "http://nginx:80"
REGISTRATION_RETRY_DELAY = 5  # seconds
MAX_RETRIES = 30  # 5 seconds * 30 = 2.5 minutes max wait

app = FastAPI(
    title="WkCrawler API",
    description="WkCrawler Plugin API",
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

class Topic(BaseModel):
    english_text: str

class TopicResult(BaseModel):
    translation: Dict[str, str]
    vocabulary: List[Dict[str, str]]

# Store results by job ID
results: Dict[str, Optional[TopicResult]] = {}

# Gemini API key
gemini_api_key = None

@app.post("/v1/topic")
async def create_topic(topic: Topic):
    # Check if we can upgrade to Gemini
    if not gemini_api_key and isinstance(app.state.llm_provider, OllamaProvider):
        if await get_gemini_api_key():
            logger.info("Upgrading to Gemini LLM provider...")
            app.state.llm_provider = LLMFactory.create(gemini_api_key)
    
    job_id = str(uuid.uuid4())
    
    # Store None initially to indicate job is in progress
    results[job_id] = None
    
    # Start processing in background
    asyncio.create_task(process_topic(job_id, topic.english_text))
    
    return {"job_id": job_id}

@app.get("/v1/topic/{job_id}")
async def get_topic(job_id: str):
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
        
    result = results[job_id]
    if result is None:
        return {"status": "processing"}
        
    return {
        "status": "complete",
        "result": result
    }

@app.get("/image")
async def get_image():
    return FileResponse(PLUGIN_IMAGE)

async def process_topic(job_id: str, english_text: str):
    """Process the topic using the agent."""
    try:
        agent = TopicExplorerAgent(llm_provider=app.state.llm_provider)
        result = await agent.run(english_text)
        results[job_id] = result
    except Exception as e:
        # Store error result
        results[job_id] = {"error": str(e)}

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
    app.state.llm_provider = LLMFactory.create(api_key)
