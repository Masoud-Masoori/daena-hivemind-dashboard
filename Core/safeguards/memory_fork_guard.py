def detect_fork(mem_log):
    return any("split" in m for m in mem_log)

if __name__ == "__main__":
    log = ["stable", "split_detected"]
    print("[Memory Fork ]:", detect_fork(log))
