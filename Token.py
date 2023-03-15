import string


class Token:
    def __init__(self, type, value=None):
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

'''
Methods
1. separate each word in a list
2. tokenize
3. merge tokens into declarations
'''
DIGITS = '0123456789'
LETTERS = string.ascii_letters
CHARS = LETTERS + DIGITS + '_'

KEYWORDS = [
    'place',
    'tran',
    'amm',
    'cap'
]

# TOKENS

TT_LBRACKET = 'LBRACKET'
TT_RBRACKET = 'RBRACKET'
TT_KEYWORD = 'KEYWORD'
TT_COMMA = 'COMMA'
TT_NEWLINE = 'NEWLINE'
TT_DOT = 'DOT'
TT_EQUAL = 'EQUAL'
TT_COLON = 'COLON'
TT_SEMICOLON = 'SEMICOLON'

def declaration_splitter(code_string: str):
    declarations = code_string.replace('\n','').split(';')[:-1]
    for declaration in declarations:
        print(declaration)

example = open("petrinets/example.txt", 'r')
declaration_splitter(example.read())