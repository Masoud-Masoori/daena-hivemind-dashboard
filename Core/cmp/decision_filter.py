def smart_decision_filter(task, cost, legal_risk):
    if cost > 1000 or legal_risk:
        print(f" Escalating {task} due to high risk or cost.")
        return False
    print(f" Approved: {task}.")
    return True
