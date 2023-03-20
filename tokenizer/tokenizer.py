import tokens as token


def is_letter(ch: str) -> bool:
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch: str) -> bool:
    return '0' <= ch <= '9'


class Tokenizer:
    def __init__(self, input: str) -> any:
        self.input: str = input  # input text
        # current position in input (points to current character)
        self.cursor: int = 0
        # current reading position in input (after current character)
        self.read_cursor: int = 0
        self.ch = ''  # current character under examination, need to see how to get byte or rune type in python3
        self.read_char()
        '''
        the reason for two pointers: we need to see further beyond the character we currently read. 
        read_cursor will always point to "next" character of input.
        cursor will always point to the character in the input that corresponds to ch byte
        '''

    '''
    Purpose of read_char method is to get next character and advance our position in input.

    IMPORTANT TO CONSIDER: supports only UTF-8, to support full Unicode range need to adapt the ch to be rune type and refactor.
    '''

    def read_char(self) -> any:
        if self.read_cursor >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.read_cursor]
        self.cursor = self.read_cursor
        self.read_cursor += 1

    def next_token(self) -> any:
        tok: Token = Token(token.EOF, "")
        self.consume_whitespace()

        # daca nu intelegi ce se intampla ibu eu cum sa explic ...
        if self.ch == "=":
            tok = Token(token.ASSIGN, self.ch)
        elif self.ch == ':':
            tok = Token(token.HUIOZNAET, self.ch)
        elif self.ch == ';':
            tok = Token(token.SEMICOLON, self.ch)
        elif self.ch == ')':
            tok = Token(token.RPAREN, self.ch)
        elif self.ch == '(':
            tok = Token(token.LPAREN, self.ch)
        elif self.ch == ',':
            tok = Token(token.COMMA, self.ch)
        elif self.ch == '.':
            tok = Token(token.DOT, self.ch)
        elif self.ch == '{':
            tok = Token(token.LBRACE, self.ch)
        elif self.ch == '}':
            tok = Token(token.RBRACE, self.ch)
        elif self.ch == 0:
            tok = Token(token.EOF, "")
        else:
            if is_letter(self.ch):
                tok.literal = self.read_identifier()
                tok.type = token.lookup_ident(tok.literal)
                return tok
            elif is_digit(self.ch):
                tok.literal = self.read_number()
                tok.type = token.INT
                return tok

            tok = Token(token.ILLEGAL, self.ch)

        self.read_char()

        return tok

    def read_identifier(self) -> str:
        cursor: int = self.cursor

        while is_letter(self.ch):
            self.read_char()

        return self.input[cursor: self.cursor]

    def read_number(self) -> str:
        cursor: int = self.cursor

        while is_digit(self.ch):
            self.read_char()

        return self.input[cursor: self.cursor]

    def consume_whitespace(self) -> any:
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.read_char()


TokenType = str


class Token:
    def __init__(self, type: TokenType, literal: str) -> any:
        self.type = type
        self.literal = literal

    def __str__(self) -> str:
        return f'Type: {self.type} | Literal: {self.literal} '
