# skill_retarget_engine.py

agent_skills = {}

def assign_skill(agent_id, skill):
    if agent_id not in agent_skills:
        agent_skills[agent_id] = set()
    agent_skills[agent_id].add(skill)

def get_skills(agent_id):
    return list(agent_skills.get(agent_id, set()))
