def select_best(source_a, source_b, mode="majority"):
    if mode == "majority":
        return source_a if len(source_a) > len(source_b) else source_b
    return "[Selector] Invalid mode"

if __name__ == "__main__":
    print(select_best("Gemini version is verbose", "OpenAI version is clear"))
