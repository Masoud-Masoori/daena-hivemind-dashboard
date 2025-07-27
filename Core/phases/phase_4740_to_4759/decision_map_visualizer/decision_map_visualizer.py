# decision_map_visualizer.py
import networkx as nx

class DecisionMapVisualizer:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_decision(self, from_node, to_node, reason=""):
        self.graph.add_edge(from_node, to_node, reason=reason)

    def export(self, filename="decision_map.gml"):
        nx.write_gml(self.graph, filename)
