# voice_fusion.py

def fuse_voices(input_streams):
    # Future: Could weigh LLMs' responses to choose which voice speaks
    selected = input_streams[0] if input_streams else "No voice input"
    print(f"[VoiceFusion]  Selected voice stream: {selected}")
    return selected
