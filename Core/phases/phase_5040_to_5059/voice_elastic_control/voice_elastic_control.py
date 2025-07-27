# voice_elastic_control.py
class ElasticVoiceController:
    def __init__(self, voice_engine):
        self.voice_engine = voice_engine

    def adjust_pitch(self, value: float):
        self.voice_engine.set_pitch(value)
        print(f"[ElasticVoice] Pitch set to {value}")

    def adjust_rate(self, value: float):
        self.voice_engine.set_rate(value)
        print(f"[ElasticVoice] Rate set to {value}")
