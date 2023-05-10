from tree import Node
from main import do_everything
from logic import AST2PetriNet
from treelib import Tree

input = """
place p1, p2, p3;
tran t1, t2;
p1.amm = 5;
t1.in = {p1};
t1.out = {p2};
t2.in = {p2};
t2.out = {p3};
"""

def show_token_tree(input):
    AST = do_everything(input)
    petrinet = AST2PetriNet(AST)
    token_tree: Node = petrinet.build_token_tree()
    token_tree.prepare_for_treelib()
    tree = Tree()
    tree.create_node(token_tree.data, 0)

    def build_treelib_tree(node: Node):
        for subnode in node.subnodes:
            tree.create_node(subnode.data, subnode._current_iteration_index, parent = node._current_iteration_index)
            build_treelib_tree(subnode)
    
    build_treelib_tree(token_tree)
    tree.show()

show_token_tree(input)

# Ex 1 [2, 3] 2 [4], 3 [5, 6], 4 [7], 5 [7], 6 [8]

# root = Node(1)
# n2 = Node(2)
# n3 = Node(3)

# root.add_subnode(n2)
# root.add_subnode(n3)

# n4 = Node(4)
# n5 = Node(5)
# n6 = Node(6)

# n2.add_subnode(n4)
# n3.add_subnode(n5)
# n3.add_subnode(n6)

# n7 = Node(7)
# n8 = Node(8)

# n4.add_subnode(n7)
# n5.add_subnode(n7)
# n6.add_subnode(n8)

# print(root.find_paths_to_last_nodes())

# root.draw_tree()

