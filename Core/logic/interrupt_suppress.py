def suppress_interrupt(user_input, current_thought):
    if len(user_input) < 4:
        return "[Suppressor]  Ignored  too short"
    if user_input.lower() in current_thought.lower():
        return "[Suppressor]  Loop prevented"
    return "[Suppressor]  Forwarded"

if __name__ == "__main__":
    print(suppress_interrupt("yes", "We are processing your command"))
