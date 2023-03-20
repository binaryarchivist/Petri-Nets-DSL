from tokenizer import Tokenizer


class TestTokenizer:
    def test_next_token(self) -> any:
        input: str = """
        place p1, p2;
        tran t1, t2;
        p1.amm = 3;
        p2.cap = 4;
        t1.out = {p1 : 2, p2};
        p1.out = {t2 : 5};"""

        tokenizer: Tokenizer = Tokenizer(input)
        tok = tokenizer.next_token()

        while tok.type != 'EOF':
            print(tok)
            tok = tokenizer.next_token()


test: TestTokenizer = TestTokenizer()

test.test_next_token()
