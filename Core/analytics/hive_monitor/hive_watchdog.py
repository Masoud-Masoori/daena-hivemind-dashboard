def hive_watchdog(metrics):
    alerts = [m for m in metrics if m["status"] != "ok"]
    return {"alerts_triggered": len(alerts), "alert_list": alerts}

if __name__ == "__main__":
    data = [{"dept": "Lingo", "status": "ok"}, {"dept": "Finance", "status": "err"}]
    print("[Watchdog] ", hive_watchdog(data))
