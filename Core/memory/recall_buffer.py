import json

class PhaseRecallBuffer:
    def __init__(self, buffer_file="core/memory/recall_buffer.json"):
        self.buffer_file = buffer_file
        try:
            with open(self.buffer_file, "r") as f:
                self.data = json.load(f)
        except:
            self.data = {}

    def save_phase(self, phase, context):
        self.data[phase] = context
        with open(self.buffer_file, "w") as f:
            json.dump(self.data, f)

    def retrieve(self, phase):
        return self.data.get(phase, None)
