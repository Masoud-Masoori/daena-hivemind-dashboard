def trace_feedback(task, score):
    return f"[TraceLog] Task: {task}, Score: {score}, Feedback: {'Positive' if score > 7 else 'Improve'}"

if __name__ == "__main__":
    print(trace_feedback("Summarize PDF", 6.9))
