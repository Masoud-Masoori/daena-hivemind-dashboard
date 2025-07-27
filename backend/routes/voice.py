"""
Voice routes for Daena AI VP System
Handles voice interaction, TTS, STT, and voice commands
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from fastapi.responses import Response
from typing import Optional, Dict, List
import logging

from backend.services.voice_service import voice_service, VoiceProvider
from backend.services.llm_service import llm_service
from backend.routes.auth import get_current_user_optional, require_permission
from backend.services.auth_service import User

router = APIRouter(prefix="/api/v1/voice", tags=["Voice"])
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_voice_status():
    """Get voice service status and capabilities"""
    try:
        status = await voice_service.get_voice_status()
        return status
    except Exception as e:
        logger.error(f"Voice status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get voice status")

@router.post("/tts")
async def text_to_speech(
    text: str = Form(...),
    provider: Optional[VoiceProvider] = Form(None),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Convert text to speech audio"""
    try:
        if not voice_service.is_voice_enabled():
            raise HTTPException(status_code=503, detail="Voice service not available")
        
        # Check permissions for non-guest users
        if current_user and hasattr(current_user, 'role'):
            if current_user.role.value == "guest" and len(text) > 100:
                raise HTTPException(status_code=403, detail="Guest users limited to 100 characters")
        
        audio_data = await voice_service.text_to_speech(text, provider)
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate speech")
        
        # Return audio response
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail="Text-to-speech failed")

@router.post("/stt")
async def speech_to_text(
    audio: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Convert speech audio to text"""
    try:
        if not voice_service.is_voice_enabled():
            raise HTTPException(status_code=503, detail="Voice service not available")
        
        # Read audio data
        audio_data = await audio.read()
        
        # Convert to text
        text = await voice_service.speech_to_text(audio_data)
        
        if not text:
            raise HTTPException(status_code=400, detail="Could not understand audio")
        
        return {
            "text": text,
            "confidence": 0.95,  # Placeholder confidence score
            "language": "en-US"
        }
        
    except Exception as e:
        logger.error(f"STT error: {e}")
        raise HTTPException(status_code=500, detail="Speech-to-text failed")

@router.post("/voice-command")
async def process_voice_command(
    audio: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Process complete voice command - STT + AI response + TTS"""
    try:
        if not voice_service.is_voice_enabled():
            raise HTTPException(status_code=503, detail="Voice service not available")
        
        # Read audio data
        audio_data = await audio.read()
        
        # Convert speech to text
        command_text = await voice_service.speech_to_text(audio_data)
        if not command_text:
            raise HTTPException(status_code=400, detail="Could not understand voice command")
        
        logger.info(f"Voice command received: {command_text}")
        
        # Process command with Daena AI
        ai_response = await llm_service.generate_response(
            prompt=command_text,
            context={"type": "voice_command", "user": current_user.username if current_user else "anonymous"}
        )
        
        # Convert AI response to speech
        response_audio = await voice_service.text_to_speech(ai_response)
        
        return {
            "command": command_text,
            "response_text": ai_response,
            "has_audio": response_audio is not None,
            "audio_available": bool(response_audio)
        }
        
    except Exception as e:
        logger.error(f"Voice command processing error: {e}")
        raise HTTPException(status_code=500, detail="Voice command processing failed")

@router.post("/daena-chat")
async def daena_voice_chat(
    audio: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Direct voice chat with Daena AI VP"""
    try:
        if not voice_service.is_voice_enabled():
            raise HTTPException(status_code=503, detail="Voice service not available")
        
        # Read audio data
        audio_data = await audio.read()
        
        # Convert speech to text
        user_message = await voice_service.speech_to_text(audio_data)
        if not user_message:
            raise HTTPException(status_code=400, detail="Could not understand your message")
        
        logger.info(f"Daena voice chat: {user_message}")
        
        # Get AI response from Daena with executive context
        ai_response = await llm_service.generate_response(
            prompt=user_message,
            context={
                "type": "voice_chat",
                "user": current_user.username if current_user else "anonymous",
                "role": current_user.role.value if current_user else "guest",
                "system": "Daena AI VP"
            }
        )
        
        # Convert response to speech
        response_audio = await voice_service.text_to_speech(ai_response)
        
        if response_audio:
            return Response(
                content=response_audio,
                media_type="audio/wav",
                headers={
                    "Content-Disposition": "attachment; filename=daena_response.wav",
                    "X-Response-Text": ai_response,
                    "X-Command-Text": user_message
                }
            )
        else:
            return {
                "command": user_message,
                "response": ai_response,
                "error": "Audio generation failed"
            }
        
    except Exception as e:
        logger.error(f"Daena voice chat error: {e}")
        raise HTTPException(status_code=500, detail="Voice chat failed")

@router.post("/listen-activation")
async def listen_for_activation(
    timeout: int = 5,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Listen for voice activation phrases"""
    try:
        if not voice_service.is_voice_enabled():
            raise HTTPException(status_code=503, detail="Voice service not available")
        
        activation_phrase = await voice_service.listen_for_activation(timeout)
        
        return {
            "activated": activation_phrase is not None,
            "phrase": activation_phrase,
            "available_phrases": voice_service.get_activation_phrases()
        }
        
    except Exception as e:
        logger.error(f"Voice activation listening error: {e}")
        raise HTTPException(status_code=500, detail="Voice activation listening failed")

@router.get("/providers")
async def get_voice_providers():
    """Get available voice providers"""
    try:
        providers = voice_service.get_available_providers()
        return {
            "providers": providers,
            "default": "system_tts",
            "recommended": "elevenlabs" if "elevenlabs" in providers else "system_tts"
        }
    except Exception as e:
        logger.error(f"Get voice providers error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get voice providers")

@router.get("/activation-phrases")
async def get_activation_phrases():
    """Get voice activation phrases"""
    try:
        phrases = voice_service.get_activation_phrases()
        return {
            "phrases": phrases,
            "count": len(phrases),
            "examples": [
                "Hey Daena, what's the company status?",
                "Jarvis, show me today's metrics",
                "Computer, start strategic meeting"
            ]
        }
    except Exception as e:
        logger.error(f"Get activation phrases error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get activation phrases")

@router.post("/test-voice")
async def test_voice_system():
    """Test voice system functionality"""
    try:
        test_text = "Hello, I'm Daena, your AI Vice President. Voice system is working correctly."
        
        # Test TTS
        audio_data = await voice_service.text_to_speech(test_text)
        tts_working = audio_data is not None
        
        # Test system status
        status = await voice_service.get_voice_status()
        
        return {
            "tts_working": tts_working,
            "stt_available": status["speech_recognition_available"],
            "providers": status["providers_available"],
            "overall_status": "working" if tts_working else "partial",
            "test_audio_generated": tts_working
        }
        
    except Exception as e:
        logger.error(f"Voice system test error: {e}")
        raise HTTPException(status_code=500, detail="Voice system test failed")

# Websocket endpoint for real-time voice interaction
@router.websocket("/ws/voice-stream")
async def voice_websocket(websocket):
    """WebSocket endpoint for real-time voice streaming"""
    await websocket.accept()
    
    try:
        while True:
            # Receive audio data
            audio_data = await websocket.receive_bytes()
            
            # Process voice command
            text = await voice_service.speech_to_text(audio_data)
            
            if text:
                # Get AI response
                ai_response = await llm_service.generate_response(text)
                
                # Send response back
                await websocket.send_json({
                    "command": text,
                    "response": ai_response,
                    "timestamp": "now"
                })
            else:
                await websocket.send_json({
                    "error": "Could not understand audio",
                    "timestamp": "now"
                })
                
    except Exception as e:
        logger.error(f"Voice WebSocket error: {e}")
        await websocket.close()

# Health check for voice service
@router.get("/health")
async def voice_health():
    """Voice service health check"""
    try:
        status = await voice_service.get_voice_status()
        return {
            "status": "healthy" if status["enabled"] else "disabled",
            "service": "voice",
            "capabilities": status
        }
    except Exception as e:
        logger.error(f"Voice health check error: {e}")
        raise HTTPException(status_code=500, detail="Voice health check failed")
