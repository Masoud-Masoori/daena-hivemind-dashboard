# contextual_regeneration_engine.py
from deep_archive_mind import DeepArchiveMind

class ContextualRegenerationEngine:
    def __init__(self):
        self.archive = DeepArchiveMind()

    def regenerate_context(self, label):
        data = self.archive.retrieve(label)
        if not data:
            return f"No archived context for {label}"
        return f"Rebuilding context for {label}... Done.\n{data}"
