import threading
import time

def deployment_daemon():
    print(" Deployment daemon started...")
    while True:
        print(" Monitoring deployment health...")
        time.sleep(60)  # Monitor every minute
