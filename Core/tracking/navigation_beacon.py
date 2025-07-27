class NavigationBeacon:
    def __init__(self, milestones=[]):
        self.milestones = milestones

    def ping(self):
        print(" Milestones ahead:")
        for m in self.milestones:
            print(f" - {m}")
