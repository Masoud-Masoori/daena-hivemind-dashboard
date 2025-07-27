# session_reconstruction.py

class SessionReconstructionKernel:
    def __init__(self):
        self.fragments = {}

    def add_fragment(self, session_id, data):
        if session_id not in self.fragments:
            self.fragments[session_id] = []
        self.fragments[session_id].append(data)

    def reconstruct(self, session_id):
        return " ".join(self.fragments.get(session_id, []))
