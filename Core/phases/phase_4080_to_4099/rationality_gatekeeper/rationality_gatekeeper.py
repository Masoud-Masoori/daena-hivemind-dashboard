# rationality_gatekeeper.py
class RationalityGatekeeper:
    def evaluate(self, decision_tree):
        try:
            return all(node.get("rationale") for node in decision_tree)
        except:
            return False
