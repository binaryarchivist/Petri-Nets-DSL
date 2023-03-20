from tokenizer import Token
import tokens as token

'''
<program> -> <declarationlist>,
<declarationlist> -> <declaration> ; <declarationlist> | ε,
<declaration> -> <instantiation> | <placefield> | <arcing>,


<instantiation> -> <type> <varlist>,
<type> -> place | tran,
<placefield> -> <var>.amm = <number> | <var>.cap = <number>,
<arcing> -> <var>.in = { <arclist> | <var>.out = { <arclist>,
<arclist> -> <arc> , <arclist> | <arc> },
<arc> -> <var> : <number> | <var>


<instantiation : type="place", names=["p1","p2"]>;
<instantiation : type="tran", names=["t1","t2"]>;
<placefield : type="amm", name="p1", val=3>;
<placefield : type="cap", name="p2", val=4>;
<arcing : type="outbound", arcs = [Arc(source="t1",destination="p1",val=3), Arc(source="t1",destination="p2",val=1)]>;
<arcing : type="inbound", arcs = [Arc(source="p1",destination="t2",val=5)]>;


<declaration : object = Instantiation(type="place", names=["p1","p2"])>
<declaration : object = Instantiation(type="tran", names=["t1","t2"])>
<declaration : object = Placefield(type="amm", name="p1", val=3)>
<declaration : object = Placefield(type="cap", name="p2", val=4)>
<declaration : object = Arcing(type="outbound", arcs = [Arc(source="t1",destination="p1",val=3), Arc(source="t1",destination="p2",val=1))>
<declaration : object = Arcing(type="inbound", arcs = [Arc(source="p1",destination="t2",val=5))>
'''

class Instantiation:
    def __init__(self, type: str, varlist: list[str] = []):
        self.type = type
        self.varlist = varlist

class Placefield:
    def __init__(self, type: str):
        self.type = type
        self.var = None
        self.val = None

class Arc:
    def __init__(self, source: str, destination: str, val: int):
        self.source = source
        self.destination = destination
        self.val = val

class Arcing:
    def __init__(self, type: str, arcs: list[Arc] = []):
        self.type = type
        self.arcs = arcs

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token = tokens[0]
        self.cursor = 0

    def next_token(self):
        self.cursor += 1
        self.current_token = self.tokens[self.cursor]
        return self.current_token

    def parsify(self):
        declaration_list = list()
        place_list = list()
        tran_list = list()
        while self.current_token != Token(token.EOF):
            while self.current_token != Token(token.SEMICOLON):
                #place instantiation
                if self.tokens[0] == Token(token.PLACE):
                    current_declaration = Instantiation(token.PLACE)
                    if self.next_token() == Token(token.IDENT):
                        while self.current_token == Token(token.IDENT):
                            current_declaration.varlist.append(self.current_token.literal)
                            place_list.append(self.current_token.literal)
                            if self.next_token() == Token(token.COMMA):
                                pass
                            else:
                                break
                            self.next_token()
                #transition instantiation
                if self.tokens[0] == Token(token.TRAN):
                    current_declaration = Instantiation(token.TRAN)
                    if self.next_token() == Token(token.IDENT):
                        while self.current_token == Token(token.IDENT):
                            current_declaration.varlist.append(self.current_token.literal)
                            tran_list.append(self.current_token.literal)
                            if self.next_token() == Token(token.COMMA):
                                pass
                            else:
                                break
                            self.next_token()
                    
                    
                
