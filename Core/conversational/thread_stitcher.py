def stitch_conversation(threads):
    return "  ".join(threads)

if __name__ == "__main__":
    conversation = ["Hello", "How can I help you?", "Please analyze this dataset"]
    print("[Stitcher] Thread:", stitch_conversation(conversation))
