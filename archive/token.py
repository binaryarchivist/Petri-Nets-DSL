import string


class Token:
    def __init__(self, type: str, value: str = None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type} : {self.value}'
        return f'{self.type}'

    def matches(self, type, value):
        return self.type == type and self.value == value

DIGITS = '0123456789'
LETTERS = string.ascii_letters
CHARS = LETTERS + DIGITS + '_'

KEYWORDS = [
    'place',
    'tran',
    'amm',
    'cap',
    'in',
    'out'
]

# TOKENS

TT_LBRACKET = 'LBRACKET'
TT_RBRACKET = 'RBRACKET'
TT_KEYWORD = 'KEYWORD'
TT_COMMA = 'COMMA'
TT_DOT = 'DOT'
TT_EQUAL = 'EQUAL'
TT_COLON = 'COLON'
TT_DATATYPE = 'DATATYPE'
TT_VAR = 'VAR'
TT_NUMBER = 'NUMBER'
TT_UNDEFINED = 'UNDEFINED'


def lbracket(value=None) -> Token:
    return Token(TT_LBRACKET)


def rbracket(value=None) -> Token:
    return Token(TT_RBRACKET)


def comma(value=None) -> Token:
    return Token(TT_COMMA)


def keyword(value: str) -> Token:
    return Token(TT_KEYWORD, value)


def dot(value=None) -> Token:
    return Token(TT_DOT)


def equal(value=None) -> Token:
    return Token(TT_EQUAL)


def colon(value=None) -> Token:
    return Token(TT_COLON)


def datatype(value: str) -> Token:
    return Token(TT_DATATYPE, value)


TOKEN_DICTIONARY = {
    '{': lbracket,
    '}': rbracket,
    ',': comma,
    '.': dot,
    '=': equal,
    ':': colon,
    'place': datatype,
    'tran': datatype,
    'amm': keyword,
    'cap': keyword,
    'in': keyword,
    'out': keyword,
}


class Lexer:

    def var_identifier(self, string):
        if string[0] not in LETTERS:
            return False
        for char in string:
            if char not in CHARS:
                return False
        return True

    def number_identifier(self, string):
        if string[0] == '0':
            return False
        for char in string:
            if char not in DIGITS:
                return False
        return True

    def token_switch(self, string):
        if string not in TOKEN_DICTIONARY:
            if self.var_identifier(string):
                return Token(TT_VAR, string)
            if self.number_identifier(string):
                return Token(TT_NUMBER, string)
            return Token(TT_UNDEFINED)
        else:
            func = TOKEN_DICTIONARY[string]
            return func(string)

    def declaration_splitter(self, code_text: str):
        return code_text.replace('\n', '').split(';')[:-1]

    def linecode_splitter(self, line_text: str):
        sequence_list = list()
        cursor1, cursor2 = 0, 0
        while cursor2 <= len(line_text):
            if cursor1 == len(line_text):
                break
            if cursor2 == len(line_text):
                sequence_list.append(line_text[cursor1:cursor2])
                cursor2 += 1
            elif line_text[cursor1] in '}{,:=.':
                sequence_list.append(line_text[cursor1])
                cursor1 = cursor2 + 1
                cursor2 = cursor1
            elif line_text[cursor2] in '}{,:=.':
                sequence_list.append(line_text[cursor1:cursor2])
                sequence_list.append(line_text[cursor2])
                cursor1 = cursor2 + 1
                cursor2 = cursor1
            elif line_text[cursor1] in ' \t\r':
                cursor1 += 1
                cursor2 += 1
            elif line_text[cursor2] in ' \t\r':
                sequence_list.append(line_text[cursor1:cursor2])
                cursor1 = cursor2
            else:
                cursor2 += 1
        return sequence_list

    def tokenize_declaration(self, declaration: str):
        return [self.token_switch(sequence) for sequence in self.linecode_splitter(declaration)]

    def tokenizer(self, code_text: list):
        return [self.tokenize_declaration(declaration) for declaration in self.declaration_splitter(code_text)]


lexer = Lexer()
example = open("example.txt", 'r').read()
print(example)
for i in lexer.tokenizer(example):
    print(i)
