class RealignmentTriggerPulse:
    def __init__(self):
        self.triggered = False

    def check_and_trigger(self, issue_flag):
        if issue_flag:
            self.triggered = True
            print(" Realignment triggered due to misfocus.")
            return True
        return False

    def reset(self):
        self.triggered = False
