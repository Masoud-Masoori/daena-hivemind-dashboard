def sync_blackout_alert(active, location):
    return f"[BlackoutSync]  {'ALERT' if active else 'Clear'} at {location}"

if __name__ == "__main__":
    print(sync_blackout_alert(True, "Finance"))
