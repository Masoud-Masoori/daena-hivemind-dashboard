class ContextPathRebuilder:
    def __init__(self):
        self.current_path = []

    def rebuild_from_snapshot(self, snapshot):
        self.current_path = snapshot.get("path", [])
        print(f" Context path rebuilt: {self.current_path}")
