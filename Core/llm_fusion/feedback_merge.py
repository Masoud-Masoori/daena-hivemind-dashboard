def merge_feedback(feedback_list):
    return " / ".join(set(feedback_list))

if __name__ == "__main__":
    print("[Merge] ", merge_feedback(["Try again", "Check syntax", "Try again"]))
