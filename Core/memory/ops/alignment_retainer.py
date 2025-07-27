def retain_alignment(mem):
    retained = [m for m in mem if "aligned" in m.lower()]
    return {"retained": retained, "count": len(retained)}

if __name__ == "__main__":
    memory = ["Aligned with ethics", "Deviation noticed", "Hard-aligned core"]
    print("[AlignRetain] ", retain_alignment(memory))
