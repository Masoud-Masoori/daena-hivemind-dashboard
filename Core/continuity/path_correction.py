def correct_path_if_drifted(expected_phase, current_phase):
    if expected_phase != current_phase:
        print(f"Drift detected: Expected {expected_phase}, but in {current_phase}. Correcting.")
        return expected_phase
    return current_phase
