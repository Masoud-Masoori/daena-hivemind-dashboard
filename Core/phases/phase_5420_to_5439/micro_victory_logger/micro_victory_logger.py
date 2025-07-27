# micro_victory_logger.py

import datetime

class MicroVictoryLogger:
    def __init__(self):
        self.victories = []

    def log(self, action):
        timestamp = datetime.datetime.now().isoformat()
        self.victories.append(f"{timestamp}: {action}")
        print(f" Victory: {action}")
