# truth_time_diffuser.py

import time

def verify_claim(agent_id, claim):
    print(f"[TruthDiffuser]  Verifying truth claim from Agent {agent_id}...")
    time.sleep(1.2)
    if 'always' in claim.lower() or 'never':
        print(f"[TruthDiffuser]  Absolutist claim detected. Weakening certainty.")
        return claim.replace('always', 'often').replace('never', 'rarely')
    return claim
