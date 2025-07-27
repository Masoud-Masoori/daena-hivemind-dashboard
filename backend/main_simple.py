from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import json
from pathlib import Path
from datetime import datetime

# Fallback settings
class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Daena"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"]
    LOG_LEVEL: str = "info"
    SECRET_KEY: str = "daena_secure_key_2025"
    TEST_API_KEY: str = "test-api-key"

settings = Settings()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "Daena Backend",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Daena status endpoint
@app.get(f"{settings.API_V1_STR}/daena/status")
async def daena_status():
    return {
        "status": "active",
        "model": "gpt-4",
        "tasks": 12,
        "performance": 98,
        "uptime": "2h 15m",
        "version": "1.0.0"
    }

# System metrics endpoint
@app.get(f"{settings.API_V1_STR}/system/metrics")
async def system_metrics():
    import psutil
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "network": 75.5,
        "agentLoad": 45.2
    }

# Mock data endpoints
@app.get(f"{settings.API_V1_STR}/agents")
async def get_agents():
    return {
        "agents": [
            {"id": "1", "name": "GPT-4 Agent", "type": "AI Assistant", "status": "active", "performance": 95},
            {"id": "2", "name": "Security Bot", "type": "Security", "status": "active", "performance": 88},
            {"id": "3", "name": "Analytics Bot", "type": "Data", "status": "active", "performance": 92}
        ]
    }

@app.get(f"{settings.API_V1_STR}/departments")
async def get_departments():
    return {
        "departments": [
            {"id": "1", "name": "AI Research", "health": "excellent", "agents": 8, "tasks": 24},
            {"id": "2", "name": "Security", "health": "good", "agents": 5, "tasks": 12},
            {"id": "3", "name": "Data Science", "health": "excellent", "agents": 6, "tasks": 18}
        ]
    }

@app.get(f"{settings.API_V1_STR}/projects")
async def get_projects():
    return {
        "projects": [
            {"id": "1", "name": "AI Model Optimization", "status": "active", "progress": 75},
            {"id": "2", "name": "Security Audit 2025", "status": "critical", "progress": 30},
            {"id": "3", "name": "Customer Analytics", "status": "active", "progress": 90}
        ]
    }

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL
    ) 