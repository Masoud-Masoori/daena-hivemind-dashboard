def log_semantics(trigger, choice):
    with open("semantic_log.txt", "a") as log:
        log.write(f"[Trigger] {trigger} => [Decision] {choice}\n")

if __name__ == "__main__":
    log_semantics("LLM disagreement", "Qwen2.5 selected")
    print("[SemanticLog] Logged.")
