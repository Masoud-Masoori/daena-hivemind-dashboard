# silent_diagnostics.py
class SilentDiagnosticKernel:
    def __init__(self):
        self.status = {}

    def run_diagnostics(self, agent_id, module_outputs):
        issues = [k for k, v in module_outputs.items() if v is None or v == "error"]
        self.status[agent_id] = "Issue Found" if issues else "Healthy"
        return issues
