def amplify_reflection(reflected):
    if "override" in reflected:
        return "AMPLIFY_ALERT"
    return "MIRRORED_SAFE"
