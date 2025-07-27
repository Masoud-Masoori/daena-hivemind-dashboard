# department_compass.py

def show_department_beacon(current_dept):
    departments = {
        "R&D": "Innovate and build.",
        "Finance": "Audit and stabilize cashflow.",
        "Security": "Guard intellectual assets.",
        "Marketing": "Amplify our voice.",
        "VoiceAI": "Empower interaction.",
        "HiveControl": "Oversee full orchestration."
    }
    beacon = departments.get(current_dept, "Unknown department.")
    print(f"[DepartmentCompass] Compass Pin: {current_dept}  {beacon}")
