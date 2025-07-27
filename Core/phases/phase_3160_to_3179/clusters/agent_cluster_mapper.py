# agent_cluster_mapper.py

SPECIALTY_CLUSTERS = {
    'finance': ['fin_analyst', 'cost_predictor'],
    'marketing': ['ad_generator', 'trend_watcher'],
    'security': ['firewall_bot', 'anomaly_checker']
}

def get_cluster_for_task(task_type):
    return SPECIALTY_CLUSTERS.get(task_type, ['generalist'])
