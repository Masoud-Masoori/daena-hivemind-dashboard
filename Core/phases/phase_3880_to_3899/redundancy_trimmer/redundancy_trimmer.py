# redundancy_trimmer.py
class RedundancyTrimmer:
    def __init__(self):
        self.last_reply = ""

    def trim(self, reply):
        if reply.strip() == self.last_reply.strip():
            return ""
        self.last_reply = reply
        return reply
