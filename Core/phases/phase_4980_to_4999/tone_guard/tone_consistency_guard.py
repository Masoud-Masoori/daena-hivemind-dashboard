# tone_consistency_guard.py
class ToneConsistencyGuard:
    def __init__(self):
        self.agent_tones = {}

    def set_agent_tone(self, agent, tone_style):
        self.agent_tones[agent] = tone_style

    def check_tone(self, agent, message):
        tone = self.agent_tones.get(agent, "neutral")
        return f"[{tone.upper()}] {message}"
