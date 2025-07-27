# error_contingency_kernel.py
class ErrorContingencyKernel:
    def detect_anomaly(self, result):
        return "error" in result or result.get("status") == "failed"

    def isolate_fault(self, log):
        return log[-1] if log else None
