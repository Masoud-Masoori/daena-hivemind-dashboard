def judge_response(llm_output, context):
    if not llm_output:
        return "Reject", 0
    if "hallucination" in llm_output.lower():
        return "Flag", 0.3
    return "Accept", 0.9
