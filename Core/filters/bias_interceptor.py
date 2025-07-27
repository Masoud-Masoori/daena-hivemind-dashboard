def intercept_bias(text):
    if "always" in text or "never" in text:
        return "[Bias]  Potential bias detected"
    return "[Bias]  Clear"

if __name__ == "__main__":
    print(intercept_bias("She never fails to impress"))
