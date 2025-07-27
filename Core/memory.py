class DaenaMemory:
    """
    Global memory for the Daena system. Could integrate a database or vector store.
    """
    def __init__(self):
        self.facts = []  # simple list to store knowledge items

    def store(self, item):
        """Store a piece of information (could be text, dict, etc.)."""
        self.facts.append(item)

    def recall(self, query=None):
        """
        Retrieve knowledge items. If query provided, return relevant items.
        Very naive search: filter by substring match.
        """
        if query is None:
            return list(self.facts)
        return [f for f in self.facts if query.lower() in str(f).lower()]
