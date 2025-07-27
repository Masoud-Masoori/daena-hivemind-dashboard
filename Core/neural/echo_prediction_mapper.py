def predict_echo_responses(sequence):
    return [f"echo::{token}" for token in sequence]
