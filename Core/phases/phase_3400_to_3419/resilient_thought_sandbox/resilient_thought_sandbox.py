# resilient_thought_sandbox.py

def isolate_and_test(thought_fn, *args, **kwargs):
    try:
        result = thought_fn(*args, **kwargs)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "failure", "error": str(e)}
