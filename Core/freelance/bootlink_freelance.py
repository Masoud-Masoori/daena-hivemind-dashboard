from core.freelance.department_freelance_bridge import map_skills_to_gigs

def startup_trigger():
    print("[Freelance Bridge]  Scanning for matches...")
    gigs = map_skills_to_gigs()
    if not gigs:
        print("No matches found.")
