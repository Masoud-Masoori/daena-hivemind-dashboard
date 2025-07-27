# forensic_trigger_hooks.py
class ForensicTriggerHooks:
    def __init__(self, alert_fn):
        self.alert_fn = alert_fn

    def trigger(self, anomaly_info):
        if "override" in anomaly_info or "tamper" in anomaly_info:
            self.alert_fn("FORCED_TRIG", anomaly_info)
