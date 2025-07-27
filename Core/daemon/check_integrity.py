import json

def check_integrity():
    try:
        with open("core/guardian/swarm_config.json") as f:
            data = json.load(f)
            assert "agents" in data
            print("[Integrity]  Guardian swarm configuration valid.")
    except Exception as e:
        print(f"[Integrity]  Failed: {e}")

if __name__ == "__main__":
    check_integrity()
