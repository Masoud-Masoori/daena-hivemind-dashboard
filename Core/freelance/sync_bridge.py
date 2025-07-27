import time

def sync_jobs_to_departments():
    jobs = ["web design", "data cleaning", "ai tutoring"]
    print(" Syncing external jobs with freelance agents...")
    for job in jobs:
        print(f" Assigning task: {job}")
        time.sleep(1)
