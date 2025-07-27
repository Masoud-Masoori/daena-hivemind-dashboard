import json

def load_tuner():
    try:
        with open("D:/Ideas/Daena/backend/tuner_config.json") as f:
            return json.load(f)
    except:
        return {}

def daena_speak(text):
    config = load_tuner()
    prefix = f"[{config.get('name', 'Daena')}  {config.get('tone', 'warm')}]"
    speak(f"{prefix}: {text}")
