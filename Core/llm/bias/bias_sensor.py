def detect_bias(response):
    bias_keywords = ["always", "never", "everyone", "no one"]
    for word in bias_keywords:
        if word in response.lower():
            return True
    return False
