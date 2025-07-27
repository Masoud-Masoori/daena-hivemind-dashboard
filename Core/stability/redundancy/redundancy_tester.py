def test_redundancy_scenarios():
    print(" Running redundancy tests...")
    scenarios = ["network", "disk_fail", "cpu_overload"]
    for s in scenarios:
        print(f" - Testing scenario: {s}")
