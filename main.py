from tokenizer import Tokenizer
from parserer import Parser
from tree import Node
from logic import do_everything,AST2PetriNet
from treelib import Tree
import json

def show_token_tree(input, max_depth=10):

    def recursion(node: Node):
        for subnode in node.subnodes:
            tree.create_node(subnode.data, subnode._current_iteration_index, parent = node._current_iteration_index)
            recursion(subnode)

    AST = do_everything(input)
    print(AST["places"])
    print(AST["trans"])
    petrinet = AST2PetriNet(AST)
    token_tree: Node = petrinet.build_token_tree(allow_reoccuring_tokens=False, _max_depth=max_depth, show_occuring_transitions=False)
    token_tree.prepare_for_treelib()
    tree = Tree()
    tree.create_node(token_tree.data, 0)
    recursion(token_tree)
    tree.show()



# input1 = """
# place p1, p2;
# p1.amm = 10;
# tran t1;
# t1.in = {p1:2};
# t1.out = {p2};
# """
#
# show_token_tree(input1)

# input2 = """
# place p1, p2, p3, p4;
# p1.amm = 1;
# tran t1, t2, t3;
# t1.in = {p1};
# t1.out = {p2,p3};
# t2.in = {p2,p3};
# t2.out = {p4};
# t3.in = {p4};
# t3.out = {p1};
# """
#
# show_token_tree(input2)
#
input3 = """
place p1;
tran t1;
t1.out = {p1};
"""

show_token_tree(input3, max_depth=30)
