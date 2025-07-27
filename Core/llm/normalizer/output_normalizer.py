import re

def normalize_output(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return "[Normalizer] " + text

if __name__ == "__main__":
    messy = "This   is    a      messy output."
    print(normalize_output(messy))
