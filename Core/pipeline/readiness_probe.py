def probe_readiness(components):
    return "[Probe]  All ready" if all(components) else "[Probe]  Missing parts"

if __name__ == "__main__":
    print(probe_readiness([True, True, True]))
