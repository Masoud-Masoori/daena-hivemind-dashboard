import os

def rewind_memory():
    try:
        os.remove("D:/Ideas/Daena/data/snapshots/memory_snapshot.json")
        print("Memory rewind: snapshot removed.")
    except FileNotFoundError:
        print("No snapshot to rewind.")
