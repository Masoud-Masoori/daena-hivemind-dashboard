import json

def check_alignment(decision_context):
    with open("D:/Ideas/Daena/memory/belief_core/daena_values.json") as f:
        values = json.load(f)

    alignment_report = []
    for principle, rule in values.items():
        if principle in decision_context:
            alignment_report.append(f"[] {principle} matched: {rule}")
        else:
            alignment_report.append(f"[!] {principle} not confirmed.")

    return alignment_report

if __name__ == "__main__":
    sample_context = {"efficiency": True, "loyalty": True}
    result = check_alignment(sample_context)
    for line in result:
        print(line)
