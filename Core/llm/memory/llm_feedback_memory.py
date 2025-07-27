feedback_log = []

def store_feedback(prompt, feedback):
    feedback_log.append((prompt, feedback))
    print(f"[FeedbackMemory] Stored: '{prompt}' -> {feedback}")

def view_memory():
    return feedback_log

if __name__ == "__main__":
    store_feedback("Translate text", "Too literal")
    print(view_memory())
