def defend_against_overload(cpu, memory):
    if cpu > 90 or memory > 90:
        print(" Overload detected! Initiating mitigation protocols...")
        return "mitigate"
    return "normal"
