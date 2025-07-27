import os
import json
import sounddevice as sd
import numpy as np
from pathlib import Path
import wave
import threading
import queue
from datetime import datetime

try:
    from TTS.api import TTS
    from TTS.utils.manage import ModelManager
except ImportError:
    TTS = None

class VoiceSpeaker:
    def __init__(self):
        self.config = self.load_config()
        self.tts_model = None
        self.audio_queue = queue.Queue()
        self.initialize_tts()
        
    def load_config(self):
        config_file = "voice_config.json"
        default_config = {
            "tts_model": "tts_models/en/vctk/vits",
            "speaker_id": "p230",
            "emotions": ["neutral", "happy", "sad", "angry"],
            "output_dir": "voice_output",
            "sample_rate": 22050
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return default_config

    def initialize_tts(self):
        if TTS is None:
            print("TTS not installed. Installing required packages...")
            os.system("pip install TTS")
            from TTS.api import TTS
            from TTS.utils.manage import ModelManager
        
        try:
            self.tts_model = TTS(model_name=self.config["tts_model"])
            print(f"Initialized TTS with model: {self.config['tts_model']}")
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            self.tts_model = None

    def speak(self, text, emotion="neutral", speaker_id=None):
        """Speak the given text with specified emotion"""
        if self.tts_model is None:
            print(f"[TTS] (Emotion={emotion}) {text}")
            return

        try:
            # Create output directory if it doesn't exist
            output_dir = Path(self.config["output_dir"])
            output_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"speech_{timestamp}.wav"
            
            # Generate speech with emotion
            wav = self.tts_model.tts(
                text=text,
                speaker_id=speaker_id or self.config["speaker_id"],
                emotion=emotion
            )
            
            # Save to file
            with wave.open(str(output_file), 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.config["sample_rate"])
                wf.writeframes(wav.tobytes())
            
            # Play the audio
            self.play_audio(wav)
            
            return str(output_file)
            
        except Exception as e:
            print(f"Error in TTS: {e}")
            return None

    def play_audio(self, wav_data):
        """Play audio data through the default audio device"""
        try:
            sd.play(wav_data, self.config["sample_rate"])
            sd.wait()
        except Exception as e:
            print(f"Error playing audio: {e}")

    def speak_async(self, text, emotion="neutral", speaker_id=None):
        """Speak text asynchronously"""
        thread = threading.Thread(
            target=self.speak,
            args=(text, emotion, speaker_id)
        )
        thread.start()
        return thread

    def stop_speaking(self):
        """Stop any ongoing speech"""
        sd.stop()

if __name__ == "__main__":
    speaker = VoiceSpeaker()
    speaker.speak("Hello, I am Daena. How can I help you today?", emotion="happy")
