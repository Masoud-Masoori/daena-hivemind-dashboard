# truth_anchor.py
class LegacyTruthAnchor:
    def __init__(self, reference_archive):
        self.reference = reference_archive

    def validate_fact(self, fact_key, proposed_value):
        true_value = self.reference.get(fact_key)
        if true_value == proposed_value:
            return " Validated"
        else:
            return f" Conflict with anchor: {fact_key} = {true_value}, not {proposed_value}"
