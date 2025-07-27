def auto_triage_log(event):
    print(" Pivot Logged:", event)
    with open("D:/Ideas/Daena/logs/pivot_log.txt", "a") as f:
        f.write(event + "\\n")
