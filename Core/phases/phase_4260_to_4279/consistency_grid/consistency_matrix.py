# consistency_matrix.py
class ConsistencyGrid:
    def __init__(self, knowledge_sources):
        self.sources = knowledge_sources

    def crosscheck(self):
        matrix = {}
        for key in self.sources[0]:
            values = [source.get(key, None) for source in self.sources]
            if len(set(values)) > 1:
                matrix[key] = values
        return matrix
