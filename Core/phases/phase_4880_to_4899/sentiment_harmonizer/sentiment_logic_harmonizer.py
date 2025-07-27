# sentiment_logic_harmonizer.py
class SentimentLogicHarmonizer:
    def harmonize(self, logic_output, sentiment_analysis):
        score = sentiment_analysis.get("score", 0)
        if score < -0.5:
            return " Critical emotional rejection"
        elif score > 0.5:
            return " Emotionally aligned with logic"
        else:
            return " Neutral  logic only"
