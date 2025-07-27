# flush_handler.py
import gc
import logging

class FlushHandler:
    def clear_unused(self):
        logging.info("Triggering garbage collection...")
        collected = gc.collect()
        logging.info(f"GC completed. Objects collected: {collected}")
        return f"Memory flush complete. Objects collected: {collected}"
