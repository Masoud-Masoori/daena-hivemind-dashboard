# thought_echo_loop.py

def echo_thought(agent_id, thought, loop_count=3):
    print(f"[EchoLoop]  Echoing for Agent {agent_id}:")
    for i in range(loop_count):
        print(f"   Echo-{i+1}: {thought}")
    return thought
