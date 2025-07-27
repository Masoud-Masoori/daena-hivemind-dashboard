# whisper_context_bridge.py

import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    print(f"[Whisper]  Transcribed: {result['text']}")
    return result['text']
