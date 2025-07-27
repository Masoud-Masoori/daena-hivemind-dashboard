# alignment_reinforcer.py
class AlignmentReinforcer:
    def __init__(self, master_objective):
        self.master = master_objective

    def check_focus(self, current_task):
        return self.master in current_task or "Reinforce: return to core objective."
