def hive_shield(nodes, breach_node):
    return {
        "breach": breach_node,
        "shield_active": True,
        "isolated_nodes": [n for n in nodes if n != breach_node]
    }

if __name__ == "__main__":
    print("[HiveShield] ", hive_shield(["A1", "A2", "A3"], "A2"))
