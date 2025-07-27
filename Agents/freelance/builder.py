import random
def build_agent(task_type):
    tools = ["python", "javascript", "api", "chatbot"]
    return f"New Freelance Agent ready for: {task_type} using {random.choice(tools)}"
