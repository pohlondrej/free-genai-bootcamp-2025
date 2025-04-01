import asyncio
import aiohttp
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Plugin configuration
PLUGIN_NAME = "example"
PLUGIN_PORT = 8001
PLUGIN_FRONTEND_PORT = 4201
MAIN_APP_URL = "http://nginx:80"
REGISTRATION_RETRY_DELAY = 5  # seconds
MAX_RETRIES = 30  # 5 seconds * 30 = 2.5 minutes max wait

async def register_plugin():
    """Register this plugin with the main application with retries"""
    plugin_data = {
        "name": PLUGIN_NAME,
        "backend_endpoint": f"http://example-backend:{PLUGIN_PORT}",
        "frontend_endpoint": f"http://example-frontend:{PLUGIN_FRONTEND_PORT}",
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

async def health_check():
    """Periodically log health status"""
    while True:
        logger.info("Plugin is healthy")
        await asyncio.sleep(30)

async def main():
    """Main entry point"""
    # First register the plugin with retries
    if not await register_plugin():
        logger.error("Plugin registration failed, exiting")
        return
    
    # Then start health checks
    await health_check()

if __name__ == "__main__":
    asyncio.run(main())
