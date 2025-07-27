def plan_strategy(goal, resources):
    return f"[Strategy]  Goal: {goal} | Resources: {', '.join(resources)}"

if __name__ == "__main__":
    print(plan_strategy("Launch Campaign", ["Agent_A", "Tool_X", "DataSet_3"]))
