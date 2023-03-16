from tokenizer import Token, Tokenizer


class TestTokenizer:
    def test_next_token(self) -> any:
        input: str = """
        place p_first, p_second;
        tran t_first, t_second;
        p_first.amm = 3;
        p_second.cap = 4;
        t_first.out = {p_first : 2, p_second};
        p_first.out = {t_second : 5};"""

        tokenizer: Tokenizer = Tokenizer(input)
        tok = tokenizer.next_token()

        while tok.type != 'EOF':
            print(tok)
            tok = tokenizer.next_token()


test: TestTokenizer = TestTokenizer()

test.test_next_token()
