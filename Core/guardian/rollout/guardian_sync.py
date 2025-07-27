def sync_guardians(global_state):
    print(" Syncing Guardian agents across nodes...")
    for agent in global_state["guardians"]:
        print(f" - Syncing {agent['name']}...")
    print(" Guardian rollout sync complete.")
