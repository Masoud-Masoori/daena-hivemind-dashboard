# memory_conflict_resolver.py
class MemoryConflictResolver:
    def resolve(self, current_facts, new_info):
        resolution = {}
        for key in new_info:
            if key in current_facts and current_facts[key] != new_info[key]:
                resolution[key] = {"previous": current_facts[key], "new": new_info[key], "conflict": True}
            else:
                resolution[key] = {"value": new_info[key], "conflict": False}
        return resolution
