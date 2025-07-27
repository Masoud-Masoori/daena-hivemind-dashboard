def adjust_behavior_model(signal_strength):
    if signal_strength < 0.5:
        print(" Adjusting behavior: Low engagement detected.")
    else:
        print(" Behavior optimal.")
