from tokenizer import Tokenizer
from parserer import Parser
from tree import Node
from logic import do_everything,AST2PetriNet
from treelib import Tree
import json


class TestTokenizer:
    def test_next_token(self) -> any:
        input: str = """
        place p1, p2, p3;
        tran t1, t2;
        p1.amm = 4;
        p2.amm = 3;
        p3.cap = 5;
        t1.in = {p1 : 2, p2 };
        p3.in = {t1 : 2};
        p3.out = {t2};
        """

        tokenizer: Tokenizer = Tokenizer(input)
        tok = tokenizer.next_token()
        tokens = [tok]


        while tok.type != 'EOF':
            tok = tokenizer.next_token()
            tokens.append(tok)
        return tokens

def show_token_tree(input):

    def recursion(node: Node):
        for subnode in node.subnodes:
            tree.create_node(subnode.data, subnode._current_iteration_index, parent = node._current_iteration_index)
            recursion(subnode)

    AST = do_everything(input)
    print(AST["places"])
    print(AST["trans"])
    petrinet = AST2PetriNet(AST)
    token_tree: Node = petrinet.build_token_tree(allow_reoccuring_tokens=True)
    token_tree.prepare_for_treelib()
    tree = Tree()
    tree.create_node(token_tree.data, 0)
    recursion(token_tree)
    tree.show()

input = """
place source, distributer, collector1, collector2;
tran connector, receiver1, receiver2;
source.amm = 5;
source.out = {connector};
connector.out = {distributer};
distributer.out = {receiver1, receiver2};
collector1.in = {receiver1};
collector2.in = {receiver2};
"""

show_token_tree(input)