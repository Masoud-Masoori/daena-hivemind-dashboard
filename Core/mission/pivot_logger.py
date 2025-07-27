import datetime

class PivotLogger:
    def __init__(self, log_file="pivot_log.txt"):
        self.log_file = log_file

    def log_pivot(self, reason, task):
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()}: PIVOT  Reason: {reason}, Interrupted Task: {task}\n")

    def recent_pivots(self):
        with open(self.log_file, "r") as f:
            return f.readlines()[-5:]
