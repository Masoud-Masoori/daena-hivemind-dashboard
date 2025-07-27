def annotate_workflow(steps):
    return [f"[Step-{i+1}]  {step}" for i, step in enumerate(steps)]

if __name__ == "__main__":
    steps = ["Initialize modules", "Run diagnostics", "Launch dashboard"]
    print(annotate_workflow(steps))
