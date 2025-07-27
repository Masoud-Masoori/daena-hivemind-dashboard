def enforce_limits(action, account):
    if action["cost"] > account["available_funds"]:
        return " Action blocked: insufficient funds"
    return " Approved"
