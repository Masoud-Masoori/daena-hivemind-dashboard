def resolve_fallback(task, attempts):
    for i, option in enumerate(attempts):
        if "fail" not in option.lower():
            return f"[Fallback]  Step {i+1}: {option}"
    return "[Fallback]  All fallback steps failed."

if __name__ == "__main__":
    print(resolve_fallback("Data Processing", ["Fail_A", "Fail_B", "Try_C"]))
