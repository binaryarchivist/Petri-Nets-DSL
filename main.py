from tokenizer import Tokenizer
from parserer import Parser
from tree import Node
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

# test: TestTokenizer = TestTokenizer()

# tokens = test.test_next_token()

# parser = Parser(tokens)
# for i in parser.parsify():
#     print(i)

# AST = parser.build_AST()
# print(json.dumps(AST, indent=4))


