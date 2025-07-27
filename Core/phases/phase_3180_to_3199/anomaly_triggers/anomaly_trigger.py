# anomaly_trigger.py

def detect_anomaly(context):
    suspicious = ['override_core', 'purge_memory', 'manual_injection']
    return any(s in context.lower() for s in suspicious)
