def clean_stale_paths(paths):
    valid = [p for p in paths if "legacy" not in p]
    return "[Cleanup]  " + str(valid)

if __name__ == "__main__":
    print(clean_stale_paths(["legacy_R1", "new_R2", "main"]))
