def resist_drift(current_focus, new_input):
    if new_input not in current_focus:
        return f"[DriftResist]  Maintaining: {current_focus}"
    return f"[DriftResist]  Adapted to: {new_input}"

if __name__ == "__main__":
    print(resist_drift("Security Check", "Entertainment"))
