import re

def clean_input(raw):
    return re.sub(r"[^\w\s]", "", raw)

if __name__ == "__main__":
    test_input = "Hello! What's up @ Daena?"
    print("[InputCleaner] ", clean_input(test_input))
