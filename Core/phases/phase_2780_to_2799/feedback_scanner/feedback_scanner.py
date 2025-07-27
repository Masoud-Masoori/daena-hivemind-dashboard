# feedback_scanner.py

def analyze_feedback(agent, feedback):
    print(f"[FeedbackScanner]  Received feedback for {agent}: '{feedback}'")
    if "slow" in feedback.lower():
        print("[FeedbackScanner]  Adjusting speed parameter...")
    elif "confused" in feedback.lower():
        print("[FeedbackScanner]  Re-routing through simplification layer...")
    elif "great" in feedback.lower():
        print("[FeedbackScanner]  Reinforcing strategy.")
