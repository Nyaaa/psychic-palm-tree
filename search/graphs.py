import random
import string
import pprint


class GenerateGraph:
    """
    Generates a random weighted graph
    Inputs:
        size: amount of nodes to generate
    """
    def __init__(self, size: int):
        self.size = size
        self.vertex_list = list(string.ascii_uppercase)[0:size]

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
            key = random.choice(self.vertex_list)
            if key not in keys:
                node = dict.fromkeys(key, random.randint(1, 10))
                keys.append(key)
                nodes.update(node)
        return nodes

    def gen_graph(self) -> dict[str, dict[str, int]]:
        """
        Adds random nodes to a dictionary, creates connections
        """
        graph = dict.fromkeys(self.vertex_list)

        for key in graph:
            rnd = random.randint(1, self.size // 4)
            graph[key] = self.gen_node(key, rnd)

        for node, links in graph.items():
            for key, value in links.items():
                graph[key][node] = value

        return graph


pp = pprint.PrettyPrinter()
gr = GenerateGraph(15)
pp.pprint(gr.gen_graph())
