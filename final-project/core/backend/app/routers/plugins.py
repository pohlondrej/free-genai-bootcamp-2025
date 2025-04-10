from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User

class PluginInfo(BaseModel):
    id: str
    name: str
    description: str
    backend_endpoint: str
    frontend_endpoint: str
    module_name: str

router = APIRouter(
    prefix="/plugins",
    tags=["plugins"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for registered plugins
_plugins = {}

@router.get("", response_model=list[PluginInfo])
async def list_plugins():
    """List all registered plugins"""
    return list(_plugins.values())

@router.post("/register", response_model=dict)
async def register_plugin(plugin: PluginInfo):
    """Register a new plugin"""
    _plugins[plugin.name] = plugin
    return {"status": "registered", "plugin": plugin}

@router.get("/gemini_key", response_model=str)
async def get_gemini_key(db: AsyncSession = Depends(get_db)):
    """Get the Gemini API key"""
    gemini_key = await User.get_setting(db, "gemini_api_key")
    if not gemini_key:
        raise HTTPException(status_code=404, detail="Gemini API key not found")
    return gemini_key

@router.get("/{plugin_id}", response_model=PluginInfo, responses={404: {"description": "Not found"}})
async def get_plugin(plugin_id: str):
    """Get plugin details by name"""
    if plugin_id not in _plugins:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return _plugins[plugin_id]
