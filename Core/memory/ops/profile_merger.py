def merge_profiles(primary, secondary):
    merged = primary.copy()
    for key, value in secondary.items():
        if key not in merged or not merged[key]:
            merged[key] = value
    return merged

if __name__ == "__main__":
    p1 = {"name": "Alpha", "language": "Python"}
    p2 = {"name": "", "location": "Canada"}
    print("[ProfileMerge] ", merge_profiles(p1, p2))
