# File: core/meta/observer.py
import datetime

class Observer:
    def log_interaction(self, agent_name, context, outcome):
        print(f"[META][{datetime.datetime.now()}] Agent: {agent_name} | Context: {context} | Outcome: {outcome}")
