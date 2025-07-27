def verify_sync_integrity(meta_status, hive_status):
    if meta_status == hive_status:
        return True
    print("Desync detected between core and hive.")
    return False
