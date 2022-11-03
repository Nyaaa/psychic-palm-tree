import random
import string
import pprint
import itertools
from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx
import search


@dataclass
class Edge:
    node1: str
    node2: str
    weight: int

    def __eq__(self, other):
        return (self.node1 == other.node1 or self.node1 == other.node2) and \
               (self.node2 == other.node1 or self.node2 == other.node2)


class GenerateGraph:
    """
    Generates a random weighted graph
    Inputs:
        size: amount of nodes to generate
    """

    def __init__(self, size: int):
        self.size = size
        self.node_list = []
        for name, i in zip(self.gen_letters(), range(self.size)):
            self.node_list.append(name)

    @staticmethod
    def gen_letters():
        for i in itertools.count(1):
            for p in itertools.product(string.ascii_uppercase, repeat=i):
                yield ''.join(p)

    def gen_node(self, key: str, num: int = 1) -> dict[str, int]:
        """
        Generates a dictionary of random weighted nodes
        Inputs:
            key: exclude this key
            num: amount of nodes to generate
        """
        keys = [key]
        nodes = {}
        while len(nodes) < num:
            key = random.choice(self.node_list)
            if key not in keys:
                node = dict.fromkeys(key, random.randint(1, 100))
                keys.append(key)
                nodes.update(node)
        return nodes

    def gen_graph(self) -> dict[str, dict[str, int]]:
        """
        Adds random nodes to a dictionary, creates connections
        """
        graph = dict.fromkeys(self.node_list)

        for key in graph:
            rnd = random.randint(1, self.size // 2)
            graph[key] = self.gen_node(key, 1)

        for node, links in graph.items():
            for key, value in links.items():
                graph[key][node] = value

        # self.draw(graph)
        return graph

    def draw(self, graph):
        lst = []

        for node1, links in graph.items():
            for node2, weight in links.items():
                edge = Edge(node1, node2, weight)
                if edge not in lst:
                    lst.append(edge)

        g = nx.Graph()

        for i in lst:
            g.add_edge(i.node1, i.node2, weight=i.weight)

        elarge = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] > 50]
        esmall = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] <= 50]

        pos = nx.spring_layout(g, scale=2)  # positions for all nodes
        nx.draw_networkx_nodes(g, pos, node_size=700)  # nodes
        nx.draw_networkx_edges(g, pos, edgelist=elarge, width=4)  # edges
        nx.draw_networkx_edges(g, pos, edgelist=esmall, width=4, alpha=0.5, edge_color="b", style="dashed")
        nx.draw_networkx_labels(g, pos, font_size=16, font_family="sans-serif")  # node labels
        #edge_labels = nx.get_edge_attributes(g, "weight")
        #nx.draw_networkx_edge_labels(g, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()


pp = pprint.PrettyPrinter(width=250)
gr = GenerateGraph(50)
graph1 = gr.gen_graph()
#pp.pprint(graph1)
print(gr.node_list)

node1 = random.choice(gr.node_list)
node2 = random.choice(gr.node_list)
print(search.dijkstra_queue(graph1, node1, node2))
