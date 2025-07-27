def notify_audit_log(event):
    with open("D:/Ideas/Daena/logs/audit_cmp.txt", "a") as log:
        log.write(f"[CMP AUDIT] {event}\n")
    print(f" CMP Audit Event: {event}")
