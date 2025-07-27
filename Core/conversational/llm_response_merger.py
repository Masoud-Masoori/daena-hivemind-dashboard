def merge_responses(responses: list):
    return max(responses, key=len)

if __name__ == "__main__":
    sample = ["Qwen: Yes.", "Yi-6B: Affirmative, the results align.", "DeepSeek: True."]
    print("[LLMMerge] Winning Response:", merge_responses(sample))
