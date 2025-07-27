def rebalance_priorities(tasks):
    print("[REBALANCER] Rebalancing task priorities...")
    # Simple example: reorder by urgency or impact
    return sorted(tasks, key=lambda t: t.get("urgency", 0), reverse=True)
