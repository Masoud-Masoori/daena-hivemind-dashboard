# checkpoint_trigger.py
import os

CHECKPOINT_FILE = "D:/Ideas/Daena/core/checkpoints/trigger_state.txt"

def save_checkpoint(note=""):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        f.write(f"Checkpoint: {note}")
    print("[CheckpointTrigger] Checkpoint saved.")
