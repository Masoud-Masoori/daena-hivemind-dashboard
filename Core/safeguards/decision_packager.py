def package_decision(result, trace):
    return {"output": result, "justification": trace}

if __name__ == "__main__":
    print("[Package ]:", package_decision("Allow", "based on threshold"))
