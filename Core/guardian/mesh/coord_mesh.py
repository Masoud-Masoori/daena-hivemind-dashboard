import json

def init_mesh():
    return {
        "mesh_id": "coord-mesh-001",
        "status": "active",
        "nodes": ["node_a", "node_b", "node_c"]
    }

if __name__ == "__main__":
    with open("core/guardian/mesh/coord_mesh.json", "w") as f:
        json.dump(init_mesh(), f, indent=2)
