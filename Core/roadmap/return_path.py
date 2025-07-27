class ReturnPath:
    def __init__(self, roadmap):
        self.roadmap = roadmap

    def rebuild_path(self, last_known_good):
        print(f" Rebuilding path from: {last_known_good}")
        return self.roadmap.get("milestones", [])[self.roadmap["milestones"].index(last_known_good):]
