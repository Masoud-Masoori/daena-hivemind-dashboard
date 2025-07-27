def trigger_breakpoint(agent, step_id, error_msg):
    print(f"[Breakpoint]  {agent} halted at Step {step_id} due to: {error_msg}")
    # Optional future: raise Exception(f"{agent} error at Step {step_id}")
