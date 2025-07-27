# pivot_compass.py
import os

HISTORY_LOG = "D:/Ideas/Daena/logs/pivot_history.log"

def record_pivot(reason, return_to):
    with open(HISTORY_LOG, 'a') as log:
        log.write(f"[Pivot] Reason: {reason} | Will return to: {return_to}\n")
    print(f"[PivotCompass] Pivot recorded. Return path: {return_to}")
