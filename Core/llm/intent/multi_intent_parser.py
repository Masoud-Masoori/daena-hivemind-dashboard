def parse_intents(text):
    if " and " in text or "," in text:
        return text.split(" and ")
    return [text]

if __name__ == "__main__":
    print("[IntentParser]", parse_intents("Check email and send report"))
