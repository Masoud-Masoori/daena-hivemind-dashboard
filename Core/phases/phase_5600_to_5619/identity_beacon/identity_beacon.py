# identity_beacon.py

class IdentityBeacon:
    def __init__(self, style, ethics, tone):
        self.style = style
        self.ethics = ethics
        self.tone = tone

    def embed_identity(self, message):
        return f"[Style: {self.style}] [Tone: {self.tone}] [Ethics: {self.ethics}]\n{message}"
