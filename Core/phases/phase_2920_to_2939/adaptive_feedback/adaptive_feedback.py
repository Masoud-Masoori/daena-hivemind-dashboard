# adaptive_feedback.py

feedback_memory = {}

def adapt_response(agent_id, response_quality):
    if agent_id not in feedback_memory:
        feedback_memory[agent_id] = []
    feedback_memory[agent_id].append(response_quality)
    if len(feedback_memory[agent_id]) > 10:
        feedback_memory[agent_id].pop(0)
    avg_quality = sum(feedback_memory[agent_id]) / len(feedback_memory[agent_id])
    print(f"[AdaptiveFeedback]  Agent {agent_id} avg response quality: {avg_quality:.2f}")
    return avg_quality
