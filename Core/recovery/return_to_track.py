class ReturnToTrack:
    def __init__(self):
        self.fix_point = None
        self.active = False

    def set_fix_point(self, label):
        self.fix_point = label
        self.active = True
        print(f" Fix point set at: {label}")

    def resume_after_fix(self):
        if self.active:
            print(f" Resuming workflow from: {self.fix_point}")
            self.active = False
        else:
            print("No active fix point found.")
