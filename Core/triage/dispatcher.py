# core/triage/dispatcher.py
from agents.registry import get_specialist

def route_task(task):
    if task['priority'] == 'urgent':
        return get_specialist('response')
    if 'code' in task['type']:
        return get_specialist('developer')
    return get_specialist('default')
