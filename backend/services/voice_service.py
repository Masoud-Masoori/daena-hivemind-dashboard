"""
Voice Service for Daena AI VP System
Handles text-to-speech, speech recognition, and voice activation
"""

import asyncio
import json
import logging
import base64
import io
from typing import Dict, List, Optional, Union, BinaryIO
from enum import Enum
import aiofiles
import tempfile
import os

# Try to import voice libraries
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from backend.config.settings import settings

logger = logging.getLogger(__name__)

class VoiceProvider(str, Enum):
    ELEVENLABS = "elevenlabs"
    GOOGLE_TTS = "google_tts"
    SYSTEM_TTS = "system_tts"

class VoiceService:
    def __init__(self):
        self.enabled = settings.voice_enabled if hasattr(settings, 'voice_enabled') else True
        self.activation_phrases = getattr(settings, 'voice_activation_phrases', ["Hey Daena", "Jarvis", "Computer"])
        
        # Initialize speech recognition
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            logger.info("✅ Speech recognition initialized")
        else:
            logger.warning("⚠️ Speech recognition not available. Install: pip install SpeechRecognition pyaudio")
        
        # Initialize TTS engine
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.8)
                voices = self.tts_engine.getProperty('voices')
                if voices and len(voices) > 1:
                    # Try to use a female voice if available
                    self.tts_engine.setProperty('voice', voices[1].id)
                logger.info("✅ System TTS initialized")
            except Exception as e:
                logger.error(f"❌ System TTS initialization failed: {e}")
                self.tts_engine = None
        else:
            logger.warning("⚠️ System TTS not available. Install: pip install pyttsx3")
            self.tts_engine = None
    
    async def text_to_speech(self, text: str, provider: Optional[VoiceProvider] = None) -> Optional[bytes]:
        """Convert text to speech audio"""
        if not self.enabled:
            return None
            
        if not provider:
            provider = VoiceProvider.SYSTEM_TTS
        
        try:
            if provider == VoiceProvider.ELEVENLABS and settings.elevenlabs_api_key:
                return await self._elevenlabs_tts(text)
            elif provider == VoiceProvider.GOOGLE_TTS and settings.google_tts_api_key:
                return await self._google_tts(text)
            elif provider == VoiceProvider.SYSTEM_TTS and self.tts_engine:
                return await self._system_tts(text)
            else:
                # Fallback to any available provider
                if settings.elevenlabs_api_key:
                    return await self._elevenlabs_tts(text)
                elif self.tts_engine:
                    return await self._system_tts(text)
                else:
                    logger.warning("No TTS providers available")
                    return None
                    
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return None
    
    async def _elevenlabs_tts(self, text: str) -> Optional[bytes]:
        """Generate speech using ElevenLabs API"""
        try:
            if not REQUESTS_AVAILABLE:
                logger.error("Requests library not available for ElevenLabs")
                return None
                
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # Rachel voice
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": settings.elevenlabs_api_key
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(url, json=data, headers=headers)
            )
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"ElevenLabs API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None
    
    async def _google_tts(self, text: str) -> Optional[bytes]:
        """Generate speech using Google TTS"""
        try:
            # Google TTS implementation would go here
            # For now, fallback to system TTS
            logger.info("Google TTS not yet implemented, using system TTS")
            return await self._system_tts(text)
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return None
    
    async def _system_tts(self, text: str) -> Optional[bytes]:
        """Generate speech using system TTS"""
        try:
            if not self.tts_engine:
                return None
            
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generate speech to file
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._generate_system_speech(text, temp_path)
            )
            
            # Read the generated audio file
            if os.path.exists(temp_path):
                async with aiofiles.open(temp_path, 'rb') as f:
                    audio_data = await f.read()
                
                # Clean up temporary file
                os.unlink(temp_path)
                return audio_data
            else:
                return None
                
        except Exception as e:
            logger.error(f"System TTS error: {e}")
            return None
    
    def _generate_system_speech(self, text: str, output_path: str):
        """Generate speech using pyttsx3 (blocking operation)"""
        try:
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"System speech generation error: {e}")
    
    async def speech_to_text(self, audio_data: bytes) -> Optional[str]:
        """Convert speech audio to text"""
        if not self.enabled or not SPEECH_RECOGNITION_AVAILABLE:
            return None
        
        try:
            # Create temporary file for audio data
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # Convert audio to text
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(
                None,
                lambda: self._recognize_speech(temp_path)
            )
            
            # Clean up temporary file
            os.unlink(temp_path)
            return text
            
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def _recognize_speech(self, audio_path: str) -> Optional[str]:
        """Recognize speech from audio file (blocking operation)"""
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
            
            # Use Google Speech Recognition (free)
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    async def listen_for_activation(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice activation phrases"""
        if not self.enabled or not SPEECH_RECOGNITION_AVAILABLE:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                lambda: self._listen_for_activation_blocking(timeout)
            )
        except Exception as e:
            logger.error(f"Voice activation listening error: {e}")
            return None
    
    def _listen_for_activation_blocking(self, timeout: int) -> Optional[str]:
        """Listen for activation phrases (blocking operation)"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            
            logger.info("Listening for voice activation...")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
            
            text = self.recognizer.recognize_google(audio).lower()
            
            # Check for activation phrases
            for phrase in self.activation_phrases:
                if phrase.lower() in text:
                    logger.info(f"Voice activation detected: {phrase}")
                    return phrase
            
            return None
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logger.error(f"Voice activation service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Voice activation error: {e}")
            return None
    
    async def process_voice_command(self, audio_data: bytes) -> Optional[str]:
        """Process complete voice command after activation"""
        text = await self.speech_to_text(audio_data)
        if text:
            logger.info(f"Voice command recognized: {text}")
            return text
        return None
    
    def is_voice_enabled(self) -> bool:
        """Check if voice features are enabled"""
        return self.enabled and (SPEECH_RECOGNITION_AVAILABLE or self.tts_engine is not None)
    
    def get_activation_phrases(self) -> List[str]:
        """Get list of voice activation phrases"""
        return self.activation_phrases
    
    def get_available_providers(self) -> List[str]:
        """Get list of available TTS providers"""
        providers = []
        
        if settings.elevenlabs_api_key:
            providers.append(VoiceProvider.ELEVENLABS.value)
        if settings.google_tts_api_key:
            providers.append(VoiceProvider.GOOGLE_TTS.value)
        if self.tts_engine:
            providers.append(VoiceProvider.SYSTEM_TTS.value)
            
        return providers
    
    async def get_voice_status(self) -> Dict:
        """Get voice service status"""
        return {
            "enabled": self.enabled,
            "speech_recognition_available": SPEECH_RECOGNITION_AVAILABLE,
            "tts_available": self.tts_engine is not None,
            "providers_available": self.get_available_providers(),
            "activation_phrases": self.activation_phrases,
            "elevenlabs_configured": bool(getattr(settings, 'elevenlabs_api_key', None)),
            "google_tts_configured": bool(getattr(settings, 'google_tts_api_key', None))
        }

# Global voice service instance
voice_service = VoiceService() 