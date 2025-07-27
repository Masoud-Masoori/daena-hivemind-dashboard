# Catches runtime errors and logs them
import traceback, json, time

def catch_and_log_error(err):
    log_entry = {
        "timestamp": time.time(),
        "error": str(err),
        "trace": traceback.format_exc()
    }
    with open("core/diagnostics/logs/errors.json", "a") as f:
        f.write(json.dumps(log_entry) + ",\n")
