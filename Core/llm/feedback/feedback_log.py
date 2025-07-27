def register_feedback(user_id, llm_id, response, rating):
    log_entry = {
        "user_id": user_id,
        "llm_id": llm_id,
        "response": response,
        "rating": rating
    }
    print("Logging feedback:", log_entry)
    return log_entry
