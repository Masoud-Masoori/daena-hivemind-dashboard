def feedback_net(signals):
    return {"average_confidence": sum(signals) / len(signals), "alert": any(s < 0.3 for s in signals)}

if __name__ == "__main__":
    print("[Feedback Net ]:", feedback_net([0.9, 0.85, 0.2]))
