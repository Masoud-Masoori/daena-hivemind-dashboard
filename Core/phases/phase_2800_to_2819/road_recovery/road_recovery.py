# road_recovery.py

def resume_main_road(agent_id, roadmap, current_stage):
    print(f"[RoadRecovery]  Checking if agent {agent_id} deviated...")
    if current_stage not in roadmap:
        print(f"[RoadRecovery]  Agent {agent_id} is off-course. Realigning to last valid stage.")
        return roadmap[-1]
    return current_stage
