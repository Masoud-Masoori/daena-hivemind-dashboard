def resolve_context_thread(statements):
    unique = list(dict.fromkeys(statements))
    return f"[ContextResolve]  {'  '.join(unique)}"

if __name__ == "__main__":
    print(resolve_context_thread(["init", "check", "init", "respond"]))
