# cognitive_integrity_scanner.py
class CognitiveIntegrityScanner:
    def __init__(self):
        self.rules = ["no contradiction", "no hallucination", "consistency with memory"]

    def scan(self, statement, memory=[]):
        for rule in self.rules:
            if rule == "no contradiction" and any(m for m in memory if m == f"NOT({statement})"):
                return False, "Contradiction with memory"
        return True, "Passed"
