def decouple_inference(reason):
    if "assumption" in reason:
        return "[Decoupler]  Assumption removed"
    return "[Decoupler]  Clean"

if __name__ == "__main__":
    print(decouple_inference("This is based on assumption A"))
