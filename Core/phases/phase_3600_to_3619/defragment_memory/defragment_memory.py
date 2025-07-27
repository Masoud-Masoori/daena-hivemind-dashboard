# defragment_memory.py
def defragment(mem_data):
    seen = set()
    defragged = []
    for entry in mem_data:
        if entry not in seen:
            defragged.append(entry)
            seen.add(entry)
    return defragged
