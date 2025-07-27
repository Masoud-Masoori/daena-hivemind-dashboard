# deployment_watchdog.py
import os

def is_environment_ready():
    return all([
        os.path.exists("D:/Ideas/Daena/env"),
        os.path.exists("D:/Ideas/Daena/core/dashboard"),
        os.path.exists("D:/Ideas/Daena/models")
    ])
