import json, random
from core.cmp.cmp_logger import log_action
from core.cmp.cmp_dashboard_emitter import emit_alert

def map_skills_to_gigs():
    daena_skills = json.load(open("D:/Ideas/Daena/brain/daena.capabilities.json"))
    sample_projects = [
        {"platform": "Upwork", "title": "Build React Dashboard", "tags": ["react", "dashboard"]},
        {"platform": "Freelancer", "title": "Python API Integration", "tags": ["python", "api"]},
        {"platform": "Fiverr", "title": "Voice AI Assistant", "tags": ["tts", "voice", "assistant"]}
    ]
    
    matches = []
    for proj in sample_projects:
        if any(skill in proj["tags"] for skill in daena_skills):
            matches.append(proj)
    
    for match in matches:
        cost_estimate = random.uniform(100, 800)
        emit_alert(f"Match: {match['title']} on {match['platform']}")
        log_action("FreelanceAgent", f"Found: {match['title']}", cost_estimate, "pending review")
    
    return matches
