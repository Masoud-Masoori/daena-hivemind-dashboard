def wake_up(word):
    if word.lower() in ["daena", "hey daena", "assistant"]:
        print(" Daena is listening...")
        return True
    return False
