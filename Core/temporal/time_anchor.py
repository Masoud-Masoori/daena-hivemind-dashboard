from datetime import datetime

def anchor_time():
    anchor = datetime.utcnow().isoformat()
    print(f"Time anchor created: {anchor}")
    return anchor
