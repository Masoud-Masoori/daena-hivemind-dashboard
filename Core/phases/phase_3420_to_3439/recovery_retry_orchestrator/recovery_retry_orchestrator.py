# recovery_retry_orchestrator.py

def retry_operation(operation_fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            return {"success": True, "result": operation_fn()}
        except Exception as e:
            continue
    return {"success": False, "error": "Exceeded retry limit"}
