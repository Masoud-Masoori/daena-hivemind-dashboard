def segment_convo(text, limit=80):
    if len(text) <= limit:
        return [text]
    return [text[i:i+limit] for i in range(0, len(text), limit)]

if __name__ == "__main__":
    t = "This is a very long message that needs to be segmented into digestible parts so the AI can process and summarize."
    print("[Segmentor]  Parts:", segment_convo(t))
