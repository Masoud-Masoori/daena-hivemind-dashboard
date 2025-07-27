sla_commitments = {
    "Deploy XTTS": "2025-06-06T23:59:00",
    "Connect freelance API": "2025-06-07T18:00:00"
}

def validate_sla(current_time):
    for task, deadline in sla_commitments.items():
        if current_time > deadline:
            print(f"[SLA VIOLATION] Missed: {task}")
        else:
            print(f"[ON TRACK] {task}")
