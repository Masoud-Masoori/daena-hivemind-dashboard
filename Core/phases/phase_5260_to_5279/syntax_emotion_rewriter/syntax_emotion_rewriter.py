# syntax_emotion_rewriter.py
class SyntaxEmotionRewriter:
    def rewrite(self, text, tone="neutral"):
        if tone == "warm":
            return " " + text
        elif tone == "urgent":
            return " " + text.upper()
        return text
