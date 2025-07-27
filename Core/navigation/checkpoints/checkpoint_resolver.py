import json, os

class CheckpointResolver:
    def __init__(self, checkpoint_file):
        self.checkpoint_file = checkpoint_file
        if not os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, "w") as f:
                json.dump({}, f)

    def mark_checkpoint(self, phase, note):
        with open(self.checkpoint_file, "r+") as f:
            data = json.load(f)
            data[str(phase)] = note
            f.seek(0)
            json.dump(data, f)
        print(f" Checkpoint {phase} marked.")

    def last_checkpoint(self):
        with open(self.checkpoint_file, "r") as f:
            data = json.load(f)
            if data:
                return max(data.items(), key=lambda x: int(x[0]))
            return None
