# trait_mutation.py

from agent_traits.agent_traits import AGENT_TRAITS

def mutate_traits(agent_id, feedback_status):
    if feedback_status == 'retry':
        current = AGENT_TRAITS.get(agent_id)
        if current and current['risk_level'] != 'zero':
            current['risk_level'] = 'low'
            current['style'] = 'adaptive'
            print(f"[Mutation] Mutated {agent_id} traits due to low performance.")
    return AGENT_TRAITS[agent_id]
