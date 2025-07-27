def break_loops(sequence):
    seen = set()
    output = []
    for item in sequence:
        if item in seen:
            output.append(f"[LoopBreak]  Duplicate halted: {item}")
            break
        seen.add(item)
        output.append(item)
    return output

if __name__ == "__main__":
    print(break_loops(["A", "B", "C", "B", "D"]))
