class AlertRelevanceScanner:
    def is_relevant(self, alert, context):
        if alert.lower() in context.lower():
            print(f" Alert matched context: {alert}")
            return True
        print(f" Irrelevant alert: {alert}")
        return False
