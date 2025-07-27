import os
import logging

def dispatch_intent(command: str):
    command = command.lower()
    logging.info(f"[IntentDispatcher] Received command: {command}")

    if "upload" in command:
        print("[IntentDispatcher]  Upload trigger recognized.")
        os.system("start explorer.exe D:\\Ideas\\Daena\\uploads")

    elif "download" in command:
        print("[IntentDispatcher]  Download trigger recognized.")
        os.system("start explorer.exe D:\\Ideas\\Daena\\downloads")

    elif "scrape" in command or "scraper" in command:
        print("[IntentDispatcher]  Scraper trigger recognized.")
        os.system("python agents/scraper_agent.py")

    elif "summarize" in command or "summary" in command:
        print("[IntentDispatcher]  Summary trigger recognized.")
        os.system("python agents/summarizer.py")

    elif "shutdown" in command:
        print("[IntentDispatcher]  Shutdown confirmed.")
        os.system("shutdown /s /t 5")

    else:
        print("[IntentDispatcher]  Unrecognized command.")
