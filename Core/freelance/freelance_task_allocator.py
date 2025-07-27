trust_map = {"HelixAgent": 0.92, "NovaAgent": 0.75}
def assign_task(task):
    chosen = max(trust_map.items(), key=lambda x: x[1])
    print(f"[ALLOCATOR] Assigning '{task}' to {chosen[0]} with trust {chosen[1]}")
    return chosen[0]
