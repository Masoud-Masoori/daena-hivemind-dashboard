def check_redundancy(components):
    issues = []
    for comp, status in components.items():
        if status != "online":
            issues.append(comp)
    return issues
