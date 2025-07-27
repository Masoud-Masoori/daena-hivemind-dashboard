class TrustNode:
    def __init__(self, source, verified):
        self.source = source
        self.verified = verified

    def __repr__(self):
        return f"[TrustChain]  Source: {self.source} | Verified: {self.verified}"

if __name__ == "__main__":
    node = TrustNode("Department_X", True)
    print(node)
