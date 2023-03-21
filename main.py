from tokenizer import Tokenizer
from parserer import Parser

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
for i in Parser(tokens).parsify():
    print(i)