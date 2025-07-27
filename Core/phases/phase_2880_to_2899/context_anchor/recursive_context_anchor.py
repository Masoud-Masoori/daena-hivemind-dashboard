# recursive_context_anchor.py

def anchor_context(conversation_thread, stable_reference):
    for msg in conversation_thread:
        if 'topic' in msg and msg['topic'] not in stable_reference:
            stable_reference[msg['topic']] = msg
    print(f"[Anchor]  Anchored {len(stable_reference)} stable topics.")
    return stable_reference
