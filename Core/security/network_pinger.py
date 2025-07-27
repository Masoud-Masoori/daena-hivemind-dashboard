import random

def ping_nodes(nodes):
    return {node: " Reachable" if random.choice([True, False]) else " Timeout" for node in nodes}

if __name__ == "__main__":
    print(ping_nodes(["Node_A", "Node_B", "Node_C"]))
