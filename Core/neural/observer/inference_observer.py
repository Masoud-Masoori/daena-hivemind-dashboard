def observe_inference(llm_name, confidence):
    return f"[OBSERVE] {llm_name} yielded confidence {confidence * 100:.1f}%"

if __name__ == "__main__":
    print(observe_inference("DeepSeek-R2", 0.88))
