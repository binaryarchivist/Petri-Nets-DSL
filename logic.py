import numpy as np
from tree import Node
from tokenizer import Tokenizer
from parserer import Parser

DEFAULT_MAX_DEPTH = 10

def do_everything(input):
    tokenizer = Tokenizer(input)
    tok = tokenizer.next_token()
    tokens = [tok]
    while tok.type != 'EOF':
        tok = tokenizer.next_token()
        tokens.append(tok)
    parser = Parser(tokens)
    parser.parsify()
    return parser.build_AST()

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

def str_matrix(M):
    matrix_string = "["
    for i in range(M.size):
        matrix_string += f"{M.item(i)} "
    return matrix_string[:-1] + "]"

def matrix_equal(A, B):
    if A.size != B.size:
        return False
    for i in range(A.size):
        if A.item(i) != B.item(i):
            return False
    return True

def matrix_in_list(M, M_list):
    for i in M_list:
        if matrix_equal(M,i):
            return True
    return False
    

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

        trans_truth_table = truth_dict(self.t)
        analyze_firing((1,) * self.t, False)
        return [np.matrix(_tuple) for _tuple in trans_truth_table if trans_truth_table[_tuple]]

    def build_token_tree(self, allow_reoccuring_tokens=False, _max_depth=DEFAULT_MAX_DEPTH, show_occuring_transitions=False):
        evaluated_tokens = []
        first_node = Node(M=self.M, depth=0, data=str_matrix(self.M))
        queue = [first_node]
        while queue:
            node = queue.pop(0)
            if (not matrix_in_list(node.M, evaluated_tokens) or allow_reoccuring_tokens) and node.depth < _max_depth:
                if show_occuring_transitions:
                    node.subnodes = [Node(M=node.M+U*self.A, depth=node.depth+1, data=str_matrix(node.M+U*self.A)+str_matrix(U)) for U in self.determine_possibilities(node.M) if not matrix_equal(node.M+U*self.A, node.M)]
                else:
                    node.subnodes = [Node(M=node.M+U*self.A, depth=node.depth+1, data=str_matrix(node.M+U*self.A)) for U in self.determine_possibilities(node.M) if not matrix_equal(node.M+U*self.A, node.M)]
                for subnode in node.subnodes:
                    queue.append(subnode)
                evaluated_tokens.append(node.M)
        self.token_tree = first_node  
        return first_node