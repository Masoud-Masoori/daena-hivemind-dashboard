# core/collision/resolver.py

def resolve_conflict(responses):
    ranked = sorted(responses, key=lambda r: r.get('confidence', 0), reverse=True)
    return ranked[0] if ranked else None
