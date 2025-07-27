import os
def forge_agent(name, role):
    print(f"[FORGE] Creating agent: {name} as {role}")
    agent_file = f"D:/Ideas/Daena/core/agents/{name}.py"
    with open(agent_file, "w") as f:
        f.write(f"# Auto-generated agent: {name} (role: {role})\\n")
        f.write("def act():\\n    print('Hello from agent')\\n")
