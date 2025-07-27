# mood_logger.py

import json, datetime

def log_agent_mood(agent_id, mood):
    timestamp = datetime.datetime.now().isoformat()
    mood_entry = { "agent": agent_id, "mood": mood, "time": timestamp }
    log_path = f"D:/Ideas/Daena/logs/mood_log.json"

    try:
        with open(log_path, 'r+') as file:
            data = json.load(file)
            data.append(mood_entry)
            file.seek(0)
            json.dump(data, file, indent=2)
    except FileNotFoundError:
        with open(log_path, 'w') as file:
            json.dump([mood_entry], file, indent=2)

    print(f"[MoodLogger]  Logged mood: {mood} for agent {agent_id}")
