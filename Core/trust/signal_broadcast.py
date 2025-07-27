def emit_trust_signal(source, score):
    return {
        "origin": source,
        "score": round(score, 2),
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }
