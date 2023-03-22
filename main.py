from tokenizer import Tokenizer
from parserer import Parser
import networkx as nx
import matplotlib.pyplot as plt


class TestTokenizer:
    def test_next_token(self) -> any:
        input: str = """
        place p1, p2;
        place p3, p4;
        tran t1, t2;
        p1.amm = 3;
        p2.cap = 4;
        t1.out = {p1 : 2, p2 : 3};
        p1.out = {t2 : 5};
        p2.in = {t1, t2};
        t2.in = {p3, p4};"""

        tokenizer: Tokenizer = Tokenizer(input)
        tok = tokenizer.next_token()
        tokens = [tok]

        while tok.type != 'EOF':
            tok = tokenizer.next_token()
            tokens.append(tok)
        return tokens


test: TestTokenizer = TestTokenizer()

tokens = test.test_next_token()

ast: dict = {
    "instantiation": {
        "place": [],
        "transition": []
    },
    "arcing": {
        "inbound": [],
        "outbound": []
    }
}
for i in Parser(tokens).parsify():
    if i.type == 'PLACE':
        for var in i.varlist:
            ast["instantiation"]['place'].append({
                'name': var
            })
    elif i.type == 'TRAN':
        for var in i.varlist:
            ast["instantiation"]['transition'].append({
                'name': var
            })
    elif i.type == 'inbound' or i.type == 'outbound':
        arcs = []
        for arc in i.arcs:
            arcs.append({
                'source': arc.source,
                'weight': arc.val,
                'destination': arc.destination
            })
        ast["arcing"][i.type] = arcs
    elif i.type == 'amm' or i.type == 'cap':
        for var in ast["instantiation"]["place"]:
            if i.var == var['name']:
                var.update({
                    "props": [
                        {
                            "type": i.type,
                            "val": i.val
                        }
                    ]
                })
        for var in ast["instantiation"]["transition"]:
            if i.var == var['name']:
                var.update({
                    "name": var,
                    "props": [
                        {
                            "type": i.type,
                            "val": i.val
                        }
                    ]
                })

G = nx.balanced_tree(2, 5)
pos = nx.drawing.nx_agraph.graphviz_layout(G)
G.add_node("main")
for child in ast:
    G.add_node(child)
    G.add_edge(child, "main")
    for prop in ast[child]:
        G.add_node(prop)
        G.add_edge(prop, child)

nx.draw(G, pos, with_labels=True)
plt.show()


