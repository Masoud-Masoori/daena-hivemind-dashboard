class TemporalPathStitcher:
    def __init__(self):
        self.fragments = []

    def stitch(self, fragment):
        self.fragments.append(fragment)
        print(f" Path fragment stitched: {fragment}")

    def full_thread(self):
        return "  ".join(self.fragments)
