# checkpoint_sentinel.py
def checkpoint_status(state):
    return {"timestamp": __import__("time").time(), "state": state}
