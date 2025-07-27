import datetime

def verify_temporal_stamp(expected):
    now = datetime.datetime.now().isoformat()
    return "[TemporalCheck] " if now[:10] == expected[:10] else "[TemporalCheck] "

if __name__ == "__main__":
    print(verify_temporal_stamp("2025-05-30T00:00:00"))
