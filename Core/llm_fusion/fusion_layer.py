def fuse_responses(openai_text, gemini_text):
    return f"[Fusion]  OpenAI: {openai_text}\n       Gemini: {gemini_text}"

if __name__ == "__main__":
    print(fuse_responses("I recommend action A", "I support option A with a 60% confidence"))
