# context_stitch.py
def stitch_context(memory_fragments):
    full_context = ""
    for frag in memory_fragments:
        full_context += f"[{frag['timestamp']}] {frag['content']}\n"
    return full_context.strip()
