# contradiction_detector.py
class ContradictionDetector:
    def detect(self, statements):
        conflicts = []
        for i in range(len(statements)):
            for j in range(i+1, len(statements)):
                if statements[i]["claim"] == f"not {statements[j]['claim']}":
                    conflicts.append((statements[i], statements[j]))
        return conflicts
