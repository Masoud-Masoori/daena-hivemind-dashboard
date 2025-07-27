def welcome_user_with_voice(tts, lang="en"):
    greeting = {
        "en": "Welcome back, Commander. Daena is ready.",
        "fr": "Bienvenue, Commandant. Daena est prête.",
        "fa": "??? ???? ??????? ????? ????? ???."
    }
    phrase = greeting.get(lang, greeting["en"])
    print(f" Speaking: {phrase}")
    tts.speak(phrase)
