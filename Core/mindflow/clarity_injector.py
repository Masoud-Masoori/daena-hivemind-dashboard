def inject_clarity(unclear):
    return f"[Clarity]  Clarified Version: '{unclear.strip().capitalize()}.'"

if __name__ == "__main__":
    print(inject_clarity("     uncertain direction  "))
