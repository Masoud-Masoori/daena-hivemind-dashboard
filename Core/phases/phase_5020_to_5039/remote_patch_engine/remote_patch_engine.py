# remote_patch_engine.py
import os

class RemotePatchEngine:
    def __init__(self, patch_dir="D:/Ideas/Daena/patches"):
        self.patch_dir = patch_dir

    def apply_patch(self, filename):
        path = os.path.join(self.patch_dir, filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                exec(f.read())
            print(f"[PatchEngine] Patch {filename} applied.")
        else:
            print(f"[PatchEngine] Patch {filename} not found.")
