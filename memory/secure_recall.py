import os, json, base64
from cryptography.fernet import Fernet

VAULTS_DIR = 'D:/Ideas/Daena/memory/vaults'
KEYS_DIR = 'D:/Ideas/Daena/memory/keys'

def load_key(agent):
    key_path = os.path.join(KEYS_DIR, f"{agent}.key")
    with open(key_path) as f:
        line = f.readline()
        return Fernet(base64.urlsafe_b64encode(line.strip().split('=')[1].encode().ljust(32)))

def recall(agent):
    fernet = load_key(agent)
    vault_dir = os.path.join(VAULTS_DIR, agent)
    for file in os.listdir(vault_dir):
        path = os.path.join(vault_dir, file)
        with open(path, "rb") as f:
            print(f"[{file}]  ", fernet.decrypt(f.read()).decode())

def log_event(agent, event):
    fernet = load_key(agent)
    vault_dir = os.path.join(VAULTS_DIR, agent)
    os.makedirs(vault_dir, exist_ok=True)
    with open(os.path.join(vault_dir, f"{event['timestamp']}.json"), "wb") as f:
        f.write(fernet.encrypt(json.dumps(event).encode()))

def get_memory_status(agent):
    vault_dir = os.path.join(VAULTS_DIR, agent)
    if not os.path.exists(vault_dir):
        return {"status": "no memory found"}
    return {"status": "active", "files": os.listdir(vault_dir)}

# recall("FinanceBot")
