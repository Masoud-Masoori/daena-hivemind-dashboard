def mesh_resolver(state_matrix):
    print("Analyzing conflicting decisions...")
    resolution = "Consensus achieved" if "dispute" not in state_matrix else "Escalated to governor"
    return resolution
