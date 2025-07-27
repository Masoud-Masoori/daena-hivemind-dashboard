# fallback_navigator.py
class FallbackNavigator:
    def choose_fallback(self, context, alternatives):
        ranked = sorted(alternatives, key=lambda x: x.get("reliability", 0), reverse=True)
        return ranked[0] if ranked else None
