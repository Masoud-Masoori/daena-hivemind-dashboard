def validate_packet(packet):
    required_keys = {"source", "destination", "payload"}
    return required_keys.issubset(set(packet.keys()))
