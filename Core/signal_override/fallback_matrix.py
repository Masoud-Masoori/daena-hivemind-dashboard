fallback_matrix = {
    "LLM_Failure": "Switch to backup LLM (Qwen)",
    "XTTS_Failure": "Switch to fallback TTS engine",
    "Network_Loss": "Queue commands locally and retry in 60s",
    "Memory_Conflict": "Initiate memory diff reconciliation"
}

def fallback_action(event_key):
    if event_key in fallback_matrix:
        print(f"[Fallback Engaged] {fallback_matrix[event_key]}")
        return fallback_matrix[event_key]
    print("[No Fallback Defined]")
    return None
