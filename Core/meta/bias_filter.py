def detect_bias(agents):
    bias_found = [k for k, v in agents.items() if v.lower() in ("always", "never")]
    return {"bias_flags": bias_found}

if __name__ == "__main__":
    print("[Bias Filter] ", detect_bias({"Qwen": "Always", "R2": "Sometimes", "Yi": "Never"}))
