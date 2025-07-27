def inject_fault(state):
    if "stable" in state:
        return "[FaultSim]  Injecting stress test signal..."
    return "[FaultSim]  Skipped (non-stable state)"

if __name__ == "__main__":
    print(inject_fault("stable memory checkpoint"))
