# intent_vectorizer.py

from sklearn.feature_extraction.text import TfidfVectorizer

class IntentVectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, texts):
        return self.vectorizer.fit_transform(texts)

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()

    def transform(self, new_texts):
        return self.vectorizer.transform(new_texts)
