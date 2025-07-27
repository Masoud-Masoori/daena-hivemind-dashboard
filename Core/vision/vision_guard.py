def guard_vision_alignment(current_focus, mission_focus):
    if current_focus.strip().lower() != mission_focus.strip().lower():
        print(" Vision drift detected.")
        return "redirect_focus"
    return "aligned"
