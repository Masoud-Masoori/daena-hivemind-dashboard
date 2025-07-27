import asyncio
import json
from typing import Dict, Set, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "council": set(),
            "founder": set(),
            "general": set()
        }
        self.connection_info: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_type: str = "general", user_id: str = None):
        """Connect a new WebSocket client"""
        await websocket.accept()
        
        if client_type not in self.active_connections:
            client_type = "general"
        
        self.active_connections[client_type].add(websocket)
        self.connection_info[websocket] = {
            "client_type": client_type,
            "user_id": user_id,
            "connected_at": datetime.now().isoformat()
        }
        
        logger.info(f"WebSocket connected: {client_type} - {user_id}")
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "client_type": client_type,
            "timestamp": datetime.now().isoformat()
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client"""
        for client_type, connections in self.active_connections.items():
            if websocket in connections:
                connections.remove(websocket)
                break
        
        if websocket in self.connection_info:
            info = self.connection_info.pop(websocket)
            logger.info(f"WebSocket disconnected: {info['client_type']} - {info['user_id']}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific WebSocket client"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast_to_type(self, message: Dict[str, Any], client_type: str):
        """Broadcast message to all clients of specific type"""
        if client_type not in self.active_connections:
            return
        
        disconnected = set()
        for websocket in self.active_connections[client_type]:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to {client_type}: {e}")
                disconnected.add(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_to_all(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        for client_type in self.active_connections:
            await self.broadcast_to_type(message, client_type)
    
    async def send_council_update(self, department: str, update_type: str, data: Dict[str, Any]):
        """Send council-specific update to founder and council clients"""
        message = {
            "type": "council_update",
            "department": department,
            "update_type": update_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send to council clients
        await self.broadcast_to_type(message, "council")
        # Send to founder clients
        await self.broadcast_to_type(message, "founder")
    
    async def send_founder_alert(self, alert_type: str, data: Dict[str, Any]):
        """Send alert specifically to founder"""
        message = {
            "type": "founder_alert",
            "alert_type": alert_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.broadcast_to_type(message, "founder")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        stats = {}
        for client_type, connections in self.active_connections.items():
            stats[client_type] = len(connections)
        stats["total"] = sum(stats.values())
        return stats

# Global WebSocket manager instance
websocket_manager = WebSocketManager()

# WebSocket endpoint handlers
async def handle_council_websocket(websocket: WebSocket, user_id: str = None):
    """Handle council WebSocket connections"""
    await websocket_manager.connect(websocket, "council", user_id)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket_manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Council WebSocket error: {e}")
        websocket_manager.disconnect(websocket)

async def handle_founder_websocket(websocket: WebSocket, user_id: str = None):
    """Handle founder WebSocket connections"""
    await websocket_manager.connect(websocket, "founder", user_id)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket_manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Founder WebSocket error: {e}")
        websocket_manager.disconnect(websocket) 