def identity_check(name, tag):
    return name.lower() == tag.lower()

if __name__ == "__main__":
    print("[ID Enforcer ]:", identity_check("Daena", "DAENA"))
