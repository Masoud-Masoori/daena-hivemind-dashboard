freelancer_stats = {
    "HelixAgent": {"completed": 4, "income": 2100},
    "NovaAgent": {"completed": 2, "income": 850}
}
for agent, stats in freelancer_stats.items():
    print(f"{agent}: {stats['completed']} jobs, ${stats['income']} earned")
