def map_memory_drift(mem_before, mem_after):
    drift = {}
    for k in mem_before:
        if k in mem_after and mem_before[k] != mem_after[k]:
            drift[k] = (mem_before[k], mem_after[k])
    return drift
