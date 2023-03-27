from tokenizer import Tokenizer
from parserer import Parser
import pprint


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


test: TestTokenizer = TestTokenizer()

tokens = test.test_next_token()

string = ''
for i in tokens:
    string += f"[{i.type}"
    if i.literal:
        string += f":{i.literal}"
    string += ']'
print(string)

for i in Parser(tokens).parsify():
    print(i)

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
                'name': var,
                'props': []
            })
    elif i.type == 'TRAN':
        for var in i.varlist:
            ast["instantiation"]['transition'].append({
                'name': var,
                'props': []
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
                        *var["props"],
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
                        *var["props"],
                        {
                            "type": i.type,
                            "val": i.val
                        }
                    ]
                })

for child in ast:
    pprint.pprint(child)
    for prop in ast[child]:
        pprint.pprint(prop)
        pprint.pprint(ast[child][prop])




