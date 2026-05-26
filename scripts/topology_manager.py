#!/usr/bin/env python3

import networkx as nx

class TopologyManager:

    def __init__(self):
        self.graph = nx.Graph()

    def update_graph(self, positions):

        self.graph.clear()

        for i in positions:
            self.graph.add_node(i)

        for i in positions:
            for j in positions:
                if i != j:
                    d = ((positions[i]-positions[j])**2).sum()**0.5

                    if d < 5.0:
                        self.graph.add_edge(i, j)

    def print_edges(self):
        print(self.graph.edges())
