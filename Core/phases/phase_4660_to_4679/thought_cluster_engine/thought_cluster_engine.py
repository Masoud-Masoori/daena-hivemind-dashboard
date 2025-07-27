# thought_cluster_engine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

class ThoughtClusterEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.kmeans = None

    def cluster_thoughts(self, thoughts, n_clusters=3):
        X = self.vectorizer.fit_transform(thoughts)
        self.kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
        self.kmeans.fit(X)
        return self.kmeans.labels_
