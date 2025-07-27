def arbitrate_responses(responses):
    scored = [(r, len(r)) for r in responses]
    chosen = max(scored, key=lambda x: x[1])[0]
    return f"[Arbiter]  Chosen: {chosen}"

if __name__ == "__main__":
    print(arbitrate_responses(["Yes", "Likely yes due to X", "No"]))
