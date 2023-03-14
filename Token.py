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
