def log_reflection(reflection, log_path):
    with open(log_path, "a") as log_file:
        log_file.write(reflection + "\n")
