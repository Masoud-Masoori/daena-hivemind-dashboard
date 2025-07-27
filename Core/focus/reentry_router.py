class ReentryRouter:
    def __init__(self, fallback="default_task"):
        self.fallback_task = fallback

    def reroute(self, after_fix):
        print(f" Routing back to: {after_fix if after_fix else self.fallback_task}")
        return after_fix or self.fallback_task
