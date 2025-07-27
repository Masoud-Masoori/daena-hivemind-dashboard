def score_command_precision(text):
    score = min(100, max(0, len(text.strip())))
    return f"[Score]  Precision Score: {score}/100"

if __name__ == "__main__":
    print(score_command_precision("Trigger audit log refresh for Q2"))
