"""
Voice Panel Routes for Daena AI VP System
Handles voice UI and voice interaction endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from typing import Dict, Any
import os
import logging

from backend.services.auth_service import auth_service, User

router = APIRouter(prefix="/api/v1/voice-panel", tags=["voice-panel"])
security = HTTPBearer()

# Audit logging
logger = logging.getLogger(__name__)

def audit_log(action: str, user: str, details: dict):
    """Audit logging for voice panel actions"""
    logger.info(f"Voice Panel Action: {action} by {user} - {details}")

# Authentication dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    return auth_service.get_current_user(credentials)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "templates"))

@router.get("/")
async def get_voice_panel_page(request: Request):
    """Get the voice panel dashboard page"""
    return templates.TemplateResponse("voice_panel.html", {"request": request})

@router.get("/status")
async def get_voice_status(user: User = Depends(get_current_user)):
    """Get voice system status"""
    audit_log("get_voice_status", user.username, {})
    
    return {
        "success": True,
        "status": "active",
        "features": {
            "speech_recognition": True,
            "speech_synthesis": True,
            "voice_commands": True,
            "real_time_processing": True
        },
        "settings": {
            "language": "en-US",
            "voice_speed": 1.0,
            "voice_pitch": 1.0,
            "auto_speak": True
        }
    } 