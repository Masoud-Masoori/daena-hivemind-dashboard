def enforce_balance(status):
    return f"[Balance] {' Normal' if status == 'equilibrium' else ' Unstable'}"

if __name__ == "__main__":
    print(enforce_balance("disrupted"))
