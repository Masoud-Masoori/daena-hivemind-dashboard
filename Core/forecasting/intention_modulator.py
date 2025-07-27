def modulate_intention(intent, urgency):
    amplified = f"{intent.upper()} !!!" if urgency > 7 else intent.capitalize()
    return f"[IntentMod]  {amplified}"

if __name__ == "__main__":
    print(modulate_intention("launch sequence", 8))
