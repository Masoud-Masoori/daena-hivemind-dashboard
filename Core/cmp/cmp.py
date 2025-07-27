import os
from dotenv import load_dotenv

class CMP:
    def __init__(self):
        self.vault = self.load_env()
        self.status = "Initialized"
        print(f"[CMP] CMP launched with vault keys: {list(self.vault.keys())}")

    def load_env(self):
        env_path = os.path.abspath("D:/Ideas/Daena/.env")
        load_dotenv(env_path)
        return {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "GROK_API_KEY": os.getenv("GROK_API_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "DEEPSEEK_R1": os.getenv("DeepSeek_R1")
        }

    def summary(self):
        return f"CMP Vault: {', '.join(self.vault.keys())}"
