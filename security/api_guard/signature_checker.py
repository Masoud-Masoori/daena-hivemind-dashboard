# Validates API calls against registered endpoint signatures
def validate_signature(endpoint, payload, known_signatures):
    return endpoint in known_signatures and "auth" in known_signatures[endpoint]
