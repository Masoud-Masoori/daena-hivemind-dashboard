### File: core/memory/memory_consistency.py

import threading

class ThreadSafeMemory:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}

    def read(self, key):
        with self._lock:
            return self._data.get(key)

    def write(self, key, value):
        with self._lock:
            self._data[key] = value

    def delete(self, key):
        with self._lock:
            if key in self._data:
                del self._data[key]
