def run_sanity_checks(context):
    checks = [
        lambda x: isinstance(x, str),
        lambda x: len(x) < 5000,
        lambda x: not x.startswith("error")
    ]
    return all(check(context) for check in checks)

if __name__ == "__main__":
    print(run_sanity_checks("launch command"))
