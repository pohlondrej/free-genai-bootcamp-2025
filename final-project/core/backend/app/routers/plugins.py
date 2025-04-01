from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class PluginInfo(BaseModel):
    name: str
    endpoint: str
    image: str

router = APIRouter(
    prefix="/plugins",
    tags=["plugins"]
)

# In-memory storage for registered plugins
_plugins = {}

def _load_plugins() -> dict:
    """Load plugins from in-memory storage"""
    return _plugins

def _save_plugins(plugins: dict):
    """Save plugins to in-memory storage"""
    global _plugins
    _plugins = plugins

@router.post("/register")
async def register_plugin(plugin: PluginInfo):
    """Register a new plugin"""
    plugins = _load_plugins()
    
    if plugin.name in plugins:
        raise HTTPException(status_code=400, detail=f"Plugin {plugin.name} already exists")
    
    plugins[plugin.name] = {
        "endpoint": plugin.endpoint,
        "image": plugin.image
    }
    
    _save_plugins(plugins)
    return {"status": "success", "message": f"Plugin {plugin.name} registered successfully"}

@router.get("/")
async def list_plugins():
    """List all registered plugins"""
    plugins = _load_plugins()
    return [
        {"name": name, "endpoint": info["endpoint"], "image": info["image"]} 
        for name, info in plugins.items()
    ]
