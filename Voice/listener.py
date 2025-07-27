import sounddevice as sd
import queue
import threading
import numpy as np
import wave
import os
from datetime import datetime
import json
import soundfile as sf
from pathlib import Path

# Voice recognition imports
try:
    import pvporcupine
    from pvporcupine import Porcupine
except ImportError:
    pvporcupine = None

import whisper
from scipy.io import wavfile

# Configuration
CONFIG_FILE = "voice_config.json"
DEFAULT_CONFIG = {
    "wake_word": "hey daena",
    "voice_threshold": 0.5,
    "sample_rate": 16000,
    "channels": 1,
    "voice_model_path": "models/voice_model.pkl",
    "owner_voice_sample": "user_voice_sample.wav"
}

class VoiceListener:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stop_listening = False
        self.config = self.load_config()
        self.voice_model = None
        self.owner_voice_embedding = None
        self.initialize_voice_recognition()
        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return DEFAULT_CONFIG

    def initialize_voice_recognition(self):
        if pvporcupine is None:
            print("Porcupine not installed. Installing required packages...")
            os.system("pip install pvporcupine")
            import pvporcupine
        
        try:
            self.porcupine = Porcupine(
                access_key=os.getenv('PORCUPINE_ACCESS_KEY', ''),
                keywords=[self.config['wake_word']]
            )
            print(f"Initialized wake word detection for: {self.config['wake_word']}")
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
            self.porcupine = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio callback status: {status}")
        if not indata.flags["C_CONTIGUOUS"]:
            indata = indata.copy()
        self.audio_queue.put(bytes(indata))

    def save_voice_sample(self, audio_data, filename):
        """Save a voice sample for training or verification"""
        sample_path = Path("voice_samples") / filename
        sample_path.parent.mkdir(exist_ok=True)
        
        with wave.open(str(sample_path), 'wb') as wf:
            wf.setnchannels(self.config['channels'])
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(self.config['sample_rate'])
            wf.writeframes(audio_data)
        return str(sample_path)

    def verify_owner_voice(self, audio_data):
        """Verify if the voice matches the owner's voice"""
        if not os.path.exists(self.config['owner_voice_sample']):
            print("No owner voice sample found. Please record a voice sample first.")
            return False
            
        # Here we would implement voice verification
        # For now, return True as a placeholder
        return True

    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        if not self.porcupine:
            print("Wake word detection not initialized")
            return False

        print("Listening for wake word...")
        with sd.RawInputStream(
            channels=self.config['channels'],
            samplerate=self.config['sample_rate'],
            callback=self.audio_callback,
            blocksize=self.porcupine.frame_length,
            dtype="int16"
        ):
            while not self.stop_listening:
                try:
                    pcm = self.audio_queue.get(timeout=1)
                    result = self.porcupine.process(pcm)
                    
                    if result >= 0:
                        print("Wake word detected!")
                        # Record a short sample to verify owner's voice
                        audio_data = self.record_voice_sample(duration=3)
                        if self.verify_owner_voice(audio_data):
                            print("Owner voice verified!")
                            return True
                        else:
                            print("Voice not recognized as owner")
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error in wake word detection: {e}")
                    continue
        return False

    def record_voice_sample(self, duration=5):
        """Record a voice sample for the specified duration"""
        print(f"Recording {duration} seconds of audio...")
        audio_data = []
        
        def callback(indata, frames, time, status):
            if status:
                print(f"Recording status: {status}")
            audio_data.append(indata.copy())
        
        with sd.InputStream(
            channels=self.config['channels'],
            samplerate=self.config['sample_rate'],
            callback=callback
        ):
            sd.sleep(int(duration * 1000))
        
        return np.concatenate(audio_data, axis=0)

    def transcribe_live(self, duration=10):
        """Transcribe live speech for the specified duration"""
        model = whisper.load_model("base")
        print("Transcribing speech...")
        
        audio_data = self.record_voice_sample(duration)
        audio_path = self.save_voice_sample(
            audio_data.tobytes(),
            f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        )
        
        result = model.transcribe(audio_path, fp16=False)
        return result.get("text", "")

    def start_listening(self):
        """Start the voice listener"""
        try:
            while not self.stop_listening:
                if self.listen_for_wake_word():
                    text = self.transcribe_live()
                    print(f"Transcribed text: {text}")
                    # Here you would process the command
                    if text.lower().strip() in ['stop', 'exit', 'quit']:
                        self.stop_listening = True
        except KeyboardInterrupt:
            print("\nStopping voice listener...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        self.stop_listening = True
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()

if __name__ == "__main__":
    listener = VoiceListener()
    listener.start_listening()
