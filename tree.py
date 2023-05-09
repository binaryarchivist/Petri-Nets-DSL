import igraph as ig
import matplotlib.pyplot as plt
import numpy as np

def str_matrix(M):
    matrix_string = "["
    for i in range(M.size):
        matrix_string += f"{M.item(i)} "
    return matrix_string[:-1] + "]"

class Node:

    def __init__(self, M:np.matrix = None, data=None, depth=0, subnodes=[]):
        if type(M) == np.matrix:
            self.data = str_matrix(M)  
        else:
            self.data = data
        self.M = M
        self.subnodes = subnodes
        self._current_iteration_index = -1
        self.depth = depth

    def __iter__(self):
        self._current_iteration_index = -1
        return self

    def __next__(self):
        if self._current_iteration_index + 1 < len(self.subnodes):
            self._current_iteration_index += 1
            current_subnode = self.subnodes[self._current_iteration_index]
            return current_subnode

        for subnode in self.subnodes:
            try:
                return next(subnode)
            except StopIteration:
                continue

        raise StopIteration()

    def __repr__(self):
        return f"Node(data={self.data}, subnodes={self.subnodes})"

    def add_subnode(self, subnode):
        if isinstance(subnode, Node):
            self.subnodes.append(subnode)
        else:
            raise ValueError("Subnode must be an instance of Node class.")

    def find_last_nodes(self):
        last_nodes = []
        if not self.subnodes:
            last_nodes.append(self)
        else:
            for subnode in self.subnodes:
                last_nodes.extend(subnode.find_last_nodes())
        return last_nodes

    def find_paths_to_last_nodes(self, current_path=None):
        if current_path is None:
            current_path = []

        current_path.append(self.data)
        paths_to_last_nodes = []

        if not self.subnodes:
            paths_to_last_nodes.append(current_path[:])

        for subnode in self.subnodes:
            paths_to_last_nodes.extend(subnode.find_paths_to_last_nodes(current_path))

        current_path.pop()

        return paths_to_last_nodes

    def to_graph(self, graph=None, parent=None):
        if graph is None:
            graph = ig.Graph(directed=True)
            graph["name"] = []  # add a name attribute to vertices

        # add this node to graph
        graph.add_vertex(name=self.data)

        # add an edge if this node has a parent
        if parent is not None:
            parent_index = graph.vs.find(name=parent).index
            current_index = graph.vs.find(name=self.data).index
            graph.add_edge(parent_index, current_index)

        # add subnodes to graph
        for subnode in self.subnodes:
            subnode.to_graph(graph, self.data)

        return graph

    def draw_tree(self):
        graph = self.to_graph()
        layout = graph.layout_reingold_tilford(mode="in", root=[0])
        ig.plot(graph, layout=layout)