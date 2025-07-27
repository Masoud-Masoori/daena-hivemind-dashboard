# priority_realigner.py
class PriorityRealigner:
    def realign(self, current_state, pending_tasks):
        if current_state.get("emergency"):
            return sorted(pending_tasks, key=lambda t: t["urgency"], reverse=True)
        return sorted(pending_tasks, key=lambda t: t["importance"], reverse=True)
