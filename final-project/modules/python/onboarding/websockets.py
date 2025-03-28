"""WebSocket connection management for onboarding."""
from fastapi import WebSocket

class ConnectionManager:
    """Manages WebSocket connections for onboarding progress updates."""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and store a new connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a connection."""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """Send a message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_json(message)

# Global connection manager instance
manager = ConnectionManager()
