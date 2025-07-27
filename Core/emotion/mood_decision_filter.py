def adjust_decision_by_mood(mood: str, decision: str):
    if mood == "anger":
        return f"[Filtered for tone] {decision.upper()}"
    if mood == "sadness":
        return f"[Soften tone] {decision.lower()}"
    return decision

if __name__ == "__main__":
    print("[MoodFilter] Adjusted:", adjust_decision_by_mood("anger", "Please stop this task."))
