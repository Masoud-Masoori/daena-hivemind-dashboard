def route_stealth_packet(packet, mesh_nodes):
    import random
    path = random.sample(mesh_nodes, len(mesh_nodes))
    return f"[StealthRoute]  Routed through {path}"

if __name__ == "__main__":
    print(route_stealth_packet("PING", ["nodeA", "nodeB", "nodeC"]))
