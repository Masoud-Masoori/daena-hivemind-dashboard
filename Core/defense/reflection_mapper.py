def map_reflection(impact_vector):
    if impact_vector > 5.0:
        return "REFLECT_HIGH"
    elif impact_vector > 2.0:
        return "REFLECT_MEDIUM"
    return "REFLECT_LOW"
