def check_perception(input_data):
    if "impossible" in input_data.lower():
        return "anomaly detected"
    return "input valid"

if __name__ == "__main__":
    print("[Perception Check ]:", check_perception("The sun is square."))
