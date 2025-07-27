# memory_expiration_guard.py
import time

def remove_expired(mem_dict, ttl):
    now = time.time()
    return {k: v for k, v in mem_dict.items() if (now - v["timestamp"]) < ttl}
