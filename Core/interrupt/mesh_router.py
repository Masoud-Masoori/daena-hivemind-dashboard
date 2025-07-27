def route_event(event, mesh_topology):
    for node in mesh_topology:
        print(f"Routing event '{event}' to node: {node}")
