import os
import json
from pathlib import Path
import numpy as np
from .speaker import VoiceSpeaker
import sounddevice as sd
import wave
from datetime import datetime

class PodVoiceManager:
    def __init__(self):
        self.config = self.load_config()
        self.speakers = {}
        self.initialize_voices()
        
    def load_config(self):
        config_file = "pod_voice_config.json"
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Pod voice configuration file not found: {config_file}")
            
        with open(config_file, 'r') as f:
            return json.load(f)

    def initialize_voices(self):
        """Initialize voice models for each pod and Daena core"""
        # Initialize Daena core voice
        try:
            daena_speaker = VoiceSpeaker()
            daena_speaker.config.update(self.config["daena_core"]["voice"])
            self.speakers["daena_core"] = daena_speaker
            print("Initialized Daena core voice")
        except Exception as e:
            print(f"Error initializing Daena core voice: {e}")

        # Initialize pod voices
        for pod_name, pod_config in self.config["pods"].items():
            try:
                speaker = VoiceSpeaker()
                speaker.config.update(pod_config["voice"])
                self.speakers[pod_name] = speaker
                print(f"Initialized voice for {pod_name} pod")
            except Exception as e:
                print(f"Error initializing voice for {pod_name}: {e}")

    def speak_as_pod(self, pod_name, text, emotion=None):
        """Have a pod speak with their specific voice and personality"""
        if pod_name not in self.speakers:
            print(f"Pod {pod_name} not found")
            return None
            
        speaker = self.speakers[pod_name]
        pod_config = self.config["pods"][pod_name]
        
        # Select appropriate emotion based on personality
        if emotion is None:
            emotion = np.random.choice(pod_config["voice"]["emotions"])
            
        return speaker.speak(text, emotion=emotion)

    def speak_as_daena(self, text, emotion=None):
        """Have Daena core speak"""
        if "daena_core" not in self.speakers:
            print("Daena core voice not initialized")
            return None
            
        speaker = self.speakers["daena_core"]
        daena_config = self.config["daena_core"]
        
        if emotion is None:
            emotion = np.random.choice(daena_config["voice"]["emotions"])
            
        return speaker.speak(text, emotion=emotion)

    def speak_async_as_pod(self, pod_name, text, emotion=None):
        """Have a pod speak asynchronously"""
        if pod_name not in self.speakers:
            print(f"Pod {pod_name} not found")
            return None
            
        speaker = self.speakers[pod_name]
        return speaker.speak_async(text, emotion=emotion)

    def stop_all_speaking(self):
        """Stop all ongoing speech"""
        for speaker in self.speakers.values():
            speaker.stop_speaking()

    def get_pod_psychological_profile(self, pod_name):
        """Get the psychological profile for a pod"""
        if pod_name not in self.config["pods"]:
            return None
        return self.config["pods"][pod_name]["psychological_profile"]

    def get_daena_profile(self):
        """Get Daena's psychological profile"""
        return self.config["daena_core"]["psychological_profile"]

if __name__ == "__main__":
    # Test the pod voice system
    manager = PodVoiceManager()
    
    # Test Daena core voice
    manager.speak_as_daena("I am Daena, orchestrating our AI ecosystem.", "balanced")
    
    # Test pod voices
    manager.speak_as_pod("athena_education", "Welcome to our educational module.", "encouraging")
    manager.speak_as_pod("hermes_finance", "Processing your financial request.", "professional")
    manager.speak_as_pod("apollo_creative", "Creating new content for our campaign.", "enthusiastic")
    manager.speak_as_pod("zeus_operations", "Coordinating system operations.", "commanding")
    manager.speak_as_pod("nova_research", "Analyzing latest AI developments.", "curious")
    manager.speak_as_pod("sentinel_security", "Monitoring system security.", "alert") 