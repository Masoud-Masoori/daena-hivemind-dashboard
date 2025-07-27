# agent_rhythm_engine.py
import time

class AgentRhythmEngine:
    def __init__(self, base_delay=0.5):
        self.base_delay = base_delay
    
    def sync(self, pace_factor=1.0):
        time.sleep(self.base_delay * pace_factor)
