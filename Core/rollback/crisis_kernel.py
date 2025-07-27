import shutil

def rollback_to_safe_state():
    backup_path = "D:/Ideas/Daena/backups/safe_state"
    current_path = "D:/Ideas/Daena"
    print(" Rolling back to safe configuration...")
    # In real usage, this should replace critical configs, not full folder
    shutil.copytree(backup_path, current_path, dirs_exist_ok=True)
    print(" Rollback complete.")
