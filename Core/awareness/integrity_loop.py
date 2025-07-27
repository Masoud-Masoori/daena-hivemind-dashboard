def check_integrity_loop(input_data):
    if "paradox" in input_data.lower():
        print("Integrity loop triggered! Re-routing logic.")
        return False
    return True
