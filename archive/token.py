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


'''
V_N = {<program>, <declarationlist>, <declaration>, <instantiation>, <placefield>, <connection>, <type>, <varlist>, <var>, <number>, <arcing>, <arclist>, <arc>, <nonzero>, <digits>, <digit>, <alpha>, <string>, <char>}
V_T = {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,_,0,1,2,3,4,5,6,7,8,9,.,,,:,{,},=,;}
P = {
<program> -> <declarationlist>,
<declarationlist> -> <declaration> ; <declarationlist> | ε,
<declaration> -> <instantiation> | <placefield> | <arcing>,

<instantiation> -> <type> <varlist>,
<type> -> place | tran,
<placefield> -> <var>.amm = <number> | <var>.cap = <number>,
<arcing> -> <var>.in = { <arclist> | <var>.out = { <arclist>,
<arclist> -> <arc> , <arclist> | <arc> },
<arc> -> <var> : <number> | <var>,

<number> -> <nonzero><digits>,
<digits> -> <digit><digits> | ε,
<digit> -> 0|<nonzero>,
<nonzero> -> 1|2|3|4|5|6|7|8|9,

<varlist> -> <var> , <varlist> | <var>,
<var> -> <alpha><string>,
<string> -> <char><string> | ε,
<char> -> _|<digit>|<alpha>,
<alpha> -> a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z
}
'''

'''
place p1, p2;
tran t1, t2;
p1.amm = 3;
p2.cap = 4;
t1.out = {p1 : 2, p2}
p1.out = {t2 : 5}

->

#all required tokens
<datatype : name="place"> <var : name="p1"> <comma> <var : name="p2">
<datatype : name="tran">  <var : name="t1"> <comma> <var : name="t2">
<var : name="p1"> <point> <keyword : name="amm"> <equal> <number : val=3>
<var : name="p2"> <point> <keyword : name="cap"> <equal> <number : val=4>
<var : name="t1"> <point> <keyword : name="out"> <equal> <leftbracket> <var ; name="p1"> <colon> <number : val=2> <comma> <var : name="p2"> <colon> <number : val=1> <rightbracket>
<var : name="p1"> <point> <keyword : name="out"> <equal> <leftbracket> <var ; name="t2"> <colon> <number : val=5> <rightbracket>

->

<datatype : name="place"> <var : name="p1">, <var : name="p2">;
<datatype : name="tran">  <var : name="t1">, <var : name="t2">;
<var : name="p1">.amm = <number: val=3>;
<var : name="p2">.cap = <number: val=4>;
<var : name="t1">.out = {<arc : destination="p1", val=2>, <arc : destination="p2", val=1>}
<var : name="p1">.out = {<arc : destination="t2", val=5>}

->

<datatype : name="place"> <varlist : names=["p1","p2"]>;
<datatype : name="tran">  <varlist : names=["t1","t2"]>;
<var : name="p1">.amm = <number: val=3>;
<var : name="p2">.cap = <number: val=4>;
<var : name="t1">.out = <arclist : arcs = [Arc(destination="p1",val=3), Arc(destination="p2",val=1)]>
<var : name="p1">.out = <arclist : arcs = [Arc(destination="t2",val=5)]>

->

<instantiation : type="place", names=["p1","p2"]>;
<instantiation : type="tran", names=["t1","t2"]>;
<placefield : type="amm", name="p1", val=3>;
<placefield : type="cap", name="p2", val=4>;
<arcing : type="outbound", arcs = [Arc(source="t1",destination="p1",val=3), Arc(source="t1",destination="p2",val=1)]>;
<arcing : type="inbound", arcs = [Arc(source="p1",destination="t2",val=5)]>;

->

<declaration : object = Instantiation(type="place", names=["p1","p2"])>
<declaration : object = Instantiation(type="tran", names=["t1","t2"])>
<declaration : object = Placefield(type="amm", name="p1", val=3)>
<declaration : object = Placefield(type="cap", name="p2", val=4)>
<declaration : object = Arcing(type="outbound", arcs = [Arc(source="t1",destination="p1",val=3), Arc(source="t1",destination="p2",val=1))>
<declaration : object = Arcing(type="inbound", arcs = [Arc(source="p1",destination="t2",val=5))>
'''

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
