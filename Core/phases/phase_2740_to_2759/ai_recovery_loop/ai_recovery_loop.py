# ai_recovery_loop.py

from core.phases.phase_2720_to_2739.context_reclaimer.context_reclaimer import save_context
from core.phases.phase_2740_to_2759.focus_chain.focus_chain import append_focus_entry

def auto_recover(agent, last_step):
    print(f"[RecoveryLoop]  Agent '{agent}' encountered interruption at '{last_step}'. Recovering...")
    save_context(agent, last_step, reason="interruption or pivot")
    append_focus_entry(last_step, status="recovered")
    print("[RecoveryLoop]  Agent is now redirected to the original phase after recovery.")
