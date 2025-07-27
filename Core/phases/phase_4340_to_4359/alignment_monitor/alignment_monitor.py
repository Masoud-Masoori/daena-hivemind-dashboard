# alignment_monitor.py
class AlignmentMonitor:
    def check_alignment(self, current_thought, long_term_values):
        return any(val in current_thought for val in long_term_values)
