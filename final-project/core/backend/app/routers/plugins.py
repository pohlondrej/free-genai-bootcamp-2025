from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class PluginInfo(BaseModel):
    name: str
    backend_endpoint: str
    frontend_endpoint: str
    module_name: str
    image: str

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

@router.get("/{plugin_name}", response_model=PluginInfo, responses={404: {"description": "Not found"}})
async def get_plugin(plugin_name: str):
    """Get plugin details by name"""
    if plugin_name not in _plugins:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return _plugins[plugin_name]
