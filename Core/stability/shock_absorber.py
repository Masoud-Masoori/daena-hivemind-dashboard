def absorb_fluctuation(level):
    if level < 3:
        return "Stable"
    elif level < 7:
        return "Minor Adjustment"
    else:
        return "Shock Absorbed: Hive Alerted"

if __name__ == "__main__":
    for lvl in [2, 5, 9]:
        print(f"[ShockAbsorb]  Level {lvl} =>", absorb_fluctuation(lvl))
