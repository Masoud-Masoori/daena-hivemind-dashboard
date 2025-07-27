# conversation_scaffold_synthesizer.py

class ConversationScaffoldSynthesizer:
    def __init__(self):
        self.scaffolds = {}

    def add_turn(self, thread_id, speaker, message):
        if thread_id not in self.scaffolds:
            self.scaffolds[thread_id] = []
        self.scaffolds[thread_id].append({"speaker": speaker, "message": message})

    def get_scaffold(self, thread_id):
        return self.scaffolds.get(thread_id, [])
