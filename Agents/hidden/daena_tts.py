import os
import json
import numpy as np
from datetime import datetime
import torch
import torchaudio
from transformers import AutoTokenizer, AutoModel
import soundfile as sf
from pathlib import Path
import edge_tts
import asyncio
from typing import Dict, List, Optional, Union

class DaenaTTS:
    def __init__(self):
        self.config = self.load_config()
        self.voice_profiles = {}
        self.initialize_voice_profiles()
        self.current_voice = "default"
        
    def load_config(self):
        """Load TTS configuration"""
        config_file = "tts_config.json"
        default_config = {
            "voice_profiles": {
                "default": {
                    "name": "en-US-JennyNeural",
                    "style": "neutral",
                    "rate": "+0%",
                    "pitch": "+0Hz",
                    "volume": "+0%"
                },
                "professional": {
                    "name": "en-US-GuyNeural",
                    "style": "professional",
                    "rate": "-10%",
                    "pitch": "-10Hz",
                    "volume": "+0%"
                },
                "friendly": {
                    "name": "en-US-AriaNeural",
                    "style": "friendly",
                    "rate": "+5%",
                    "pitch": "+5Hz",
                    "volume": "+0%"
                },
                "empathetic": {
                    "name": "en-US-JennyNeural",
                    "style": "empathetic",
                    "rate": "-5%",
                    "pitch": "+10Hz",
                    "volume": "+0%"
                }
            },
            "emotion_mapping": {
                "happy": {
                    "style": "cheerful",
                    "rate": "+10%",
                    "pitch": "+15Hz"
                },
                "sad": {
                    "style": "sad",
                    "rate": "-10%",
                    "pitch": "-10Hz"
                },
                "angry": {
                    "style": "angry",
                    "rate": "+15%",
                    "pitch": "+20Hz"
                },
                "calm": {
                    "style": "calm",
                    "rate": "-5%",
                    "pitch": "-5Hz"
                },
                "excited": {
                    "style": "excited",
                    "rate": "+20%",
                    "pitch": "+25Hz"
                }
            },
            "output_settings": {
                "format": "mp3",
                "sample_rate": 24000,
                "channels": 1,
                "bit_depth": 16
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return default_config
        
    def initialize_voice_profiles(self):
        """Initialize voice profiles from config"""
        self.voice_profiles = self.config["voice_profiles"]
        
    async def synthesize_speech(self, text: str, voice_profile: str = "default", 
                              emotion: Optional[str] = None) -> str:
        """Synthesize speech using Edge TTS"""
        if voice_profile not in self.voice_profiles:
            voice_profile = "default"
            
        profile = self.voice_profiles[voice_profile].copy()
        
        # Apply emotion if specified
        if emotion and emotion in self.config["emotion_mapping"]:
            emotion_settings = self.config["emotion_mapping"][emotion]
            profile.update(emotion_settings)
            
        # Create output directory if it doesn't exist
        output_dir = Path("output/tts")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"daena_speech_{timestamp}.{self.config['output_settings']['format']}"
        
        # Configure communication
        communicate = edge_tts.Communicate(
            text,
            profile["name"],
            rate=profile["rate"],
            volume=profile["volume"],
            pitch=profile["pitch"],
            style=profile["style"]
        )
        
        # Synthesize speech
        await communicate.save(str(output_file))
        
        return str(output_file)
        
    def create_custom_voice_profile(self, name: str, settings: Dict) -> bool:
        """Create a custom voice profile"""
        if name in self.voice_profiles:
            return False
            
        # Validate required settings
        required_settings = ["name", "style", "rate", "pitch", "volume"]
        if not all(setting in settings for setting in required_settings):
            return False
            
        self.voice_profiles[name] = settings
        return True
        
    def update_voice_profile(self, name: str, settings: Dict) -> bool:
        """Update an existing voice profile"""
        if name not in self.voice_profiles:
            return False
            
        self.voice_profiles[name].update(settings)
        return True
        
    def delete_voice_profile(self, name: str) -> bool:
        """Delete a voice profile"""
        if name not in self.voice_profiles or name == "default":
            return False
            
        del self.voice_profiles[name]
        return True
        
    def get_available_voices(self) -> List[str]:
        """Get list of available voice profiles"""
        return list(self.voice_profiles.keys())
        
    def get_voice_settings(self, name: str) -> Optional[Dict]:
        """Get settings for a specific voice profile"""
        return self.voice_profiles.get(name)
        
    def analyze_emotion(self, text: str) -> str:
        """Analyze text to determine appropriate emotion"""
        # Simple emotion detection based on keywords
        emotion_keywords = {
            "happy": ["happy", "joy", "excited", "great", "wonderful"],
            "sad": ["sad", "sorry", "unfortunate", "regret"],
            "angry": ["angry", "frustrated", "annoyed", "upset"],
            "calm": ["calm", "peaceful", "relaxed", "serene"],
            "excited": ["excited", "thrilled", "amazing", "incredible"]
        }
        
        text = text.lower()
        emotion_scores = {emotion: 0 for emotion in emotion_keywords}
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    emotion_scores[emotion] += 1
                    
        # Return the emotion with the highest score, or "neutral" if no clear emotion
        max_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        return max_emotion[0] if max_emotion[1] > 0 else "neutral"
        
    def save_config(self):
        """Save current configuration to file"""
        config = {
            "voice_profiles": self.voice_profiles,
            "emotion_mapping": self.config["emotion_mapping"],
            "output_settings": self.config["output_settings"]
        }
        
        with open("tts_config.json", 'w') as f:
            json.dump(config, f, indent=2)
            
    async def process_text(self, text: str, voice_profile: str = "default", 
                         auto_emotion: bool = True) -> str:
        """Process text and generate speech with optional emotion detection"""
        emotion = None
        if auto_emotion:
            emotion = self.analyze_emotion(text)
            
        return await self.synthesize_speech(text, voice_profile, emotion)

async def main():
    # Test the TTS system
    tts = DaenaTTS()
    
    # Test basic speech synthesis
    text = "Hello, I am Daena. I'm here to help you with your tasks."
    output_file = await tts.synthesize_speech(text)
    print(f"Generated speech file: {output_file}")
    
    # Test emotion-based synthesis
    emotional_text = "I'm so excited to help you achieve your goals!"
    output_file = await tts.synthesize_speech(emotional_text, emotion="excited")
    print(f"Generated emotional speech file: {output_file}")
    
    # Test custom voice profile
    tts.create_custom_voice_profile("consultant", {
        "name": "en-US-JennyNeural",
        "style": "professional",
        "rate": "-5%",
        "pitch": "-5Hz",
        "volume": "+0%"
    })
    
    # Test with custom profile
    output_file = await tts.synthesize_speech(
        "As your consultant, I recommend the following strategy.",
        voice_profile="consultant"
    )
    print(f"Generated speech with custom profile: {output_file}")
    
    # Test emotion analysis
    text = "I'm really happy to see your progress!"
    emotion = tts.analyze_emotion(text)
    print(f"Detected emotion: {emotion}")
    
    # Save configuration
    tts.save_config()

if __name__ == "__main__":
    asyncio.run(main()) 