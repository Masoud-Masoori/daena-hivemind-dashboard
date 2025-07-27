# rational_chain_generator.py
class RationalChainGenerator:
    def __init__(self):
        pass

    def generate(self, input_facts):
        chain = []
        for fact in input_facts:
            chain.append(f" because '{fact}'")
        return " ".join(chain)
