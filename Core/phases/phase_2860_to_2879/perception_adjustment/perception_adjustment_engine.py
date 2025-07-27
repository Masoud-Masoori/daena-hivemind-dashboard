# perception_adjustment_engine.py

def adjust_perception(agent_view, external_feedback):
    for key, val in external_feedback.items():
        if key in agent_view:
            agent_view[key] = (agent_view[key] + val) / 2
    print(f"[PerceptionAdjuster]  Adjusted agent perception using feedback.")
    return agent_view
