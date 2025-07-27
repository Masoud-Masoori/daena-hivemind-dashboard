# execution_drift_visualizer.py

def compare_steps(expected: list, actual: list) -> str:
    diffs = [f'- {e}  {a}' for e, a in zip(expected, actual) if e != a]
    return "\n".join(diffs) if diffs else " Execution followed expected path"
