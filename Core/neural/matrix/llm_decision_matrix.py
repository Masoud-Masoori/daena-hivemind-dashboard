def llm_matrix_decision(llm_outputs):
    scores = {k: len(v.split()) for k, v in llm_outputs.items()}
    decision = max(scores, key=scores.get)
    return {"scores": scores, "final_choice": decision}

if __name__ == "__main__":
    sample = {"Qwen": "Yes, proceed with caution.", "R2": "Strongly advise against it.", "Yi": "No."}
    print("[Decision Matrix Loop]", llm_matrix_decision(sample))
