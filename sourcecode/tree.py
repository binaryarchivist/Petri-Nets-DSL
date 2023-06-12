import numpy as np

def str_matrix(M):
    matrix_string = "["
    for i in range(M.size):
        matrix_string += f"{M.item(i)} "
    return matrix_string[:-1] + "]"

class Node:

    def __init__(self, M:np.matrix = None, data=None, subnodes=[], depth=0):
        self.data = data
        self.M:np.matrix = M
        self.subnodes = subnodes
        self._current_iteration_index = -1
        self.tree_index:int
        self.depth = depth

    def prepare_for_treelib(self) -> None:

        def preorder_traversal(node: Node, number):
            node.tree_index = number
            for subnode in node.subnodes:
                number += 1
                number = preorder_traversal(subnode, number)
            return number

        preorder_traversal(self, 0)
