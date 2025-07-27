def sanitize(text):
    banned_words = ["error", "forbidden", "classified"]
    return " ".join("[REDACTED]" if word in banned_words else word for word in text.split())

if __name__ == "__main__":
    print("[Sanitizer] ", sanitize("This is a classified report with error logs."))
