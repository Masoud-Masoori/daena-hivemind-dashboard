def converge_directives(primary, alt_list):
    consensus = [d for d in alt_list if d == primary]
    confidence = len(consensus) / len(alt_list)
    return f"[Converge] Primary='{primary}' | Agreement={confidence*100:.1f}%"

if __name__ == "__main__":
    print(converge_directives("Protect", ["Protect", "Grow", "Protect", "Pause"]))
