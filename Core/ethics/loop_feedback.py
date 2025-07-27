def ethical_loop_check(intent, impact):
    if intent == "good" and impact != "harmful":
        return " Ethically sound"
    return " Ethical violation risk"

if __name__ == "__main__":
    print(ethical_loop_check("good", "neutral"))
