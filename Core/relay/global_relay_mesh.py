def start_relay_mesh():
    endpoints = ["LLM_Qwen", "LLM_DeepSeek", "LLM_Yi"]
    print("[RelayMesh] Bridging endpoints: " + ", ".join(endpoints))

if __name__ == "__main__":
    start_relay_mesh()
