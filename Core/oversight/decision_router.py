def route_decision(node, requires_approval):
    return f"[Router]  Routed to {'human' if requires_approval else 'autonomous'} node: {node}"

if __name__ == "__main__":
    print(route_decision("Marketing-LLM-Fusion", True))
