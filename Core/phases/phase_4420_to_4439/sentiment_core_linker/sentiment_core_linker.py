# sentiment_core_linker.py
from textblob import TextBlob

class SentimentCoreLinker:
    def analyze(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
