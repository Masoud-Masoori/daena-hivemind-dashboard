def automate_workflow(steps):
    return "  ".join([f"[Auto]{i+1}:{step}" for i, step in enumerate(steps)])

if __name__ == "__main__":
    print(automate_workflow(["Collect Data", "Preprocess", "Train Model", "Evaluate"]))
