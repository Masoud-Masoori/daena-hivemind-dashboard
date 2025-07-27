def build_narrative(statements):
    return " ".join(statements)

if __name__ == "__main__":
    story = build_narrative(["Daena initialized.", "Departments aligned.", "Conflict resolved."])
    print("[NarrativeBuilder] ", story)
