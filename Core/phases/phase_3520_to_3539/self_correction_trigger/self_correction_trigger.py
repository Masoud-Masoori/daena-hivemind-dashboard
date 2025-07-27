# self_correction_trigger.py

def trigger_correction(event_log, rules):
    for rule in rules:
        if rule['condition'] in event_log:
            return rule['action']
    return None
