def collect_feedback(reports):
    success = sum(1 for r in reports if "" in r)
    fail = len(reports) - success
    return f"[HiveFeedback]  Success: {success}, Fail: {fail}"

if __name__ == "__main__":
    print(collect_feedback(["agent A: ", "agent B: ", "agent C: "]))
