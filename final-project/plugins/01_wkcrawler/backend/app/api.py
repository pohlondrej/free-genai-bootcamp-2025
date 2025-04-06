from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict, List, Optional
import asyncio
import aiohttp
import logging
from agent import TopicExplorerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plugin configuration
PLUGIN_NAME = "wkcrawler"
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

async def process_topic(job_id: str, english_text: str):
    """Process the topic using the agent."""
    try:
        agent = TopicExplorerAgent()
        result = agent.run(english_text, gemini_api_key)
        
        # Store the result
        results[job_id] = result
        
    except Exception as e:
        # Store error result
        results[job_id] = {"error": str(e)}


async def register_plugin():
    """Register this plugin with the main application with retries"""
    plugin_data = {
        "name": PLUGIN_NAME,
        "backend_endpoint": f"http://localhost:{PLUGIN_PORT}",
        "frontend_endpoint": f"http://localhost:{PLUGIN_FRONTEND_PORT}",
        "module_name": "examplePlugin",
        "image": "example-plugin:latest"
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
                params={"plugin_name": PLUGIN_NAME}
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
        logger.error("${PLUGIN_NAME} registration failed, exiting...")
        exit(323)

    if not await get_gemini_api_key():
        logger.warning("Gemini API key not found, defaulting to Ollama...")
