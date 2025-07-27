# loop_control.py
recent_responses = []

def detect_loop(response, max_history=5):
    global recent_responses
    recent_responses.append(response.strip().lower())
    if len(recent_responses) > max_history:
        recent_responses.pop(0)
    return recent_responses.count(response.strip().lower()) > 2
