def sync_live_status(departments):
    for dept, status in departments.items():
        print(f"[LIVEOPS] {dept} status: {status}")
