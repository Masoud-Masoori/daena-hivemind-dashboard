def annotate_breakpoints(decision_flow):
    annotations = []
    for step in decision_flow:
        if "conflict" in step.lower():
            annotations.append((step, "Breakpoint identified"))
    return annotations
