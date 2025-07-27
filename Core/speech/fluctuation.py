def fluctuate_speech(sentence, excitement_level=0.5):
    if excitement_level > 0.7:
        return sentence.upper() + "!!"
    elif excitement_level < 0.3:
        return sentence.lower() + "..."
    return sentence
