def analyze_feedback(responses):
    positive = [r for r in responses if "" in r]
    return f"[Feedback] {len(positive)} positive / {len(responses)} total."

if __name__ == "__main__":
    print(analyze_feedback([" Good job", " Retry needed", " Well done"]))
