def adjust_precision(input_text, desired_level="high"):
    if desired_level == "high":
        return "[PrecisionAdjuster] Trimmed, focused response."
    elif desired_level == "medium":
        return "[PrecisionAdjuster] Balanced detail."
    return "[PrecisionAdjuster] Verbose explanation."

if __name__ == "__main__":
    print(adjust_precision("Explain quantum computing.", "high"))
