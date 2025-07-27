def scan_alignment(intended, predicted):
    score = sum([1 for a, b in zip(intended, predicted) if a == b]) / len(intended)
    return {"alignment_score": round(score * 100, 2)}

if __name__ == "__main__":
    print("[Alignment Score] ", scan_alignment(["A", "B", "C"], ["A", "X", "C"]))
