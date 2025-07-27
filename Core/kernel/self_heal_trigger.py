import os
def heal_daena():
    print("[HEALING] Running fallback reboot...")
    os.system("python D:/Ideas/Daena/core/autonomy/pivot_logger.py")
    os.system("python D:/Ideas/Daena/core/autonomy/department_boot.py")
