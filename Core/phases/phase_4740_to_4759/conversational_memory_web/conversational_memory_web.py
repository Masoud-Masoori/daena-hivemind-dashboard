# conversational_memory_web.py
class ConversationalMemoryWeb:
    def __init__(self):
        self.web = {}

    def link_contexts(self, source, target):
        if source not in self.web:
            self.web[source] = []
        self.web[source].append(target)

    def get_connections(self, source):
        return self.web.get(source, [])
