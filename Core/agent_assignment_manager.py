departments = {}

def assign_agent(department_name, agent_name):
    if department_name not in departments:
        print(f"[ERROR] Department {department_name} does not exist")
        return False
    departments[department_name]["agents"].append(agent_name)
    print(f"[ASSIGN] Agent {agent_name} assigned to {department_name}")
    return True
