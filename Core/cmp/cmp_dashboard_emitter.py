import json
import asyncio
from fastapi import WebSocket

connected_clients = []

async def connect(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

async def disconnect(websocket: WebSocket):
    connected_clients.remove(websocket)

async def emit_alert(message):
    for client in connected_clients:
        await client.send_text(json.dumps({"type": "alert", "message": message}))

async def emit_agent_status(agent, status):
    for client in connected_clients:
        await client.send_text(json.dumps({"type": "agent_status", "agent": agent, "status": status}))

async def emit_memory_update(agent, memory_status):
    for client in connected_clients:
        await client.send_text(json.dumps({"type": "memory_update", "agent": agent, "status": memory_status}))
