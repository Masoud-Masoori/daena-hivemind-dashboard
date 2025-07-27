def stitch_semantics(segments):
    return "[Stitcher]  " + "  ".join(segments)

if __name__ == "__main__":
    print(stitch_semantics(["Intent start", "processing detail", "conclusion"]))
