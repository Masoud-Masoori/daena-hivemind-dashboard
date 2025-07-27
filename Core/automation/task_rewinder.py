def rewind_tasks(executed):
    return executed[::-1]

if __name__ == "__main__":
    print(rewind_tasks(["Step A", "Step B", "Step C"]))
