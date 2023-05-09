import numpy as np
from main import do_everything

MAX_DEPTH = 10

def AST2PetriNet(AST: dict):
    place = AST["place"]
    places = int(len(place)/2)
    tran = AST["tran"]
    trans = int(len(tran)/2)
    arc_in = AST["arc_in"]
    arc_out = AST["arc_out"]
    M = [0] * places
    C = [0] * places
    for i in range(places):
        M[i] = place[i]["amm"]
        C[i] = place[i]["cap"]
    A_M = [[0] * places for _ in range(trans)]
    for p, t, weight in arc_in:
        A_M[t][p] = weight  
    A_P = [[0] * places for _ in range(trans)]
    for t, p, weight in arc_out:
        A_P[t][p] = weight
    return PetriNet(
        np.matrix(M),
        np.matrix(A_P),
        np.matrix(A_M),
        np.matrix(C),
        places,
        trans)

def truth_dict(a: int):
    b = 2**a
    truth_list = dict()
    for i in range(b):
        str = bin(i)[2:]
        truth_list[tuple([int(i) for i in list('0'*(a-len(str)) + str)])] = -1
    return truth_list

def less_tuple(bin_tuple):
    new_list = []
    for i in range(len(bin_tuple)):
        if bin_tuple[i]:
            temp = list(bin_tuple)
            temp[i] = 0
            new_list.append(tuple(temp))
    return new_list

def preorder_traversal(node):
    print(node.depth, node.M)
    if node.subnodes:
        for subnode in node.subnodes:
            preorder_traversal(subnode)

class Node:
    def __init__(self, M: np.matrix, depth = 0, subnodes: list = []):
        self.M = M
        self.depth = depth
        self.subnodes = subnodes
    def __str__(self):
        str = ""
        for i in self.subnodes:
            str += f"{i.M}"
        return f"{self.M} - [{str}]"

class PetriNet:

    def __init__(self, M: np.matrix, A_P: np.matrix, A_M: np.matrix, C: np.matrix, p, t):
        self.token_tree: Node
        self.M: np.matrix = M
        self.A_P: np.matrix = A_P
        self.A_M: np.matrix = A_M
        self.A = self.A_P - self.A_M
        self.C: np.matrix = C
        self.p = p
        self.t = t

    def print_petrinet(self):
        print(f"tokens:\n{self.M}")
        print(f"capacity:\n{self.C}")
        print(f"A_P:\n{self.A_P}")
        print(f"A_M:\n{self.A_M}")
        print(f"A:\n{self.A_P-self.A_M}")

    def valid_tokens(self, M: np.matrix, U: np.matrix):
        newM = M - U * self.A_M
        for i in range(newM.size):
            if newM.item(i) < 0:
                return False
        newM = newM + U * self.A_P
        for i in range(newM.size):
            if newM.item(i) > self.C.item(i):
                return False
        return True

    def determine_possibilities(self, M: np.matrix):
        trans_truth_table = truth_dict(self.t)

        def analyze_firing(current_tuple, root_state):
            if root_state:
                trans_truth_table[current_tuple] = False
                for _tuple in less_tuple(current_tuple):
                    analyze_firing(_tuple, True)
            if trans_truth_table[current_tuple] == -1:
                if self.valid_tokens(M, np.matrix(current_tuple)):
                    trans_truth_table[current_tuple] = True
                else:
                    trans_truth_table[current_tuple] = False
                for _tuple in less_tuple(current_tuple):
                    analyze_firing(_tuple, trans_truth_table[current_tuple]) 
            print(trans_truth_table) 

        analyze_firing((1,) * self.t, False)
        return [_tuple for _tuple in trans_truth_table if trans_truth_table[_tuple]]

    def build_token_tree(self):

        # def recursion_token_tree(M):
        #     possibilities = self.determine_possibilities(M)
        #     subnodes = []
        #     for U in possibilities:
        #         subnode = M + np.matrix(U) * self.A
        #         if subnode in evaluated_tokens:
        #             subnodes.append(Node(subnode))
        #         else:
        #             evaluated_tokens.append(subnode)
        #             subnodes.append(recursion_token_tree(subnode))
        #     return Node(M, subnodes)
        
        def breadth_first_token_tree():
            evaluated_tokens = []
            first_node = Node(self.M, 0)
            queue = [first_node]
            while queue:
                node = queue.pop(0)
                if node.M not in evaluated_tokens and node.depth < MAX_DEPTH:
                    node.subnodes = [Node(node.M + np.matrix(U) * self.A, node.depth+1) for U in self.determine_possibilities(node.M) if node.M + np.matrix(U) * self.A != node.M]
                    for subnode in node.subnodes:
                        queue.append(subnode)
                    evaluated_tokens.append(node.M)
            return first_node     

        # self.token_tree = recursion_token_tree(self.M)
        self.token_tree = breadth_first_token_tree()

input:str = """
place p1;
p1.amm = 1;
tran t1, t2, t3;
p1.out = {t1, t2};
p1.in = {t3};
"""

AST = do_everything(input)

tb = truth_dict(4)

petrinet = AST2PetriNet(AST)
petrinet.build_token_tree()
preorder_traversal(petrinet.token_tree)