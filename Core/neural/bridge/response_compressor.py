def compress_response(text):
    return "".join(word[0] for word in text.split())

if __name__ == "__main__":
    print("[Compress] Result:", compress_response("Autonomous agent decision validated"))
