def propagate_permission(role, permissions_map):
    print(f"Propagating permissions for role: {role}")
    return permissions_map.get(role, [])
