# domain_anchors.py
class DomainAnchor:
    def __init__(self, domain_name):
        self.domain = domain_name
        self.core_terms = []
        self.pillars = {}

    def add_pillar(self, pillar_name, description):
        self.pillars[pillar_name] = description

    def define_core_terms(self, terms):
        self.core_terms.extend(terms)
