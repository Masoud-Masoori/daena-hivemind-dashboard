def monitor_departments():
    for dept, data in departments.items():
        print(f"[HEALTH] {dept}: {len(data['agents'])} agents active")
