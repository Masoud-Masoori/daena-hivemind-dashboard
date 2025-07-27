# hallucination_filter.py
def is_hallucination(text):
    red_flags = ["as an AI language model", "I cannot browse the internet", "I'm not sure"]
    return any(flag in text.lower() for flag in red_flags)
