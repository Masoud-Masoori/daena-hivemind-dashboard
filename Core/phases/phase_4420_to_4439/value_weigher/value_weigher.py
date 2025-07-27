# value_weigher.py
class ValueWeigher:
    def __init__(self, priorities):
        self.priorities = priorities  # e.g., {"safety": 5, "efficiency": 3, "innovation": 4}

    def weigh(self, context):
        return sorted(context.items(), key=lambda item: self.priorities.get(item[0], 0), reverse=True)
