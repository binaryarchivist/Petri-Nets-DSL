from tokenizer import Token
import tokens as token

def error(message):
    raise ValueError(message)

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

    def __str__(self):
        return f"Instantiation: {self.type} {self.varlist}"

class Placefield:
    def __init__(self, type: str, var: str, val: int):
        self.type = type
        self.var = var
        self.val = val
    def __str__(self):
        return f"Placefield: {self.type} {self.var} {self.val}"

class Arc:
    def __init__(self, source: str, destination: str, val: int):
        self.source = source
        self.destination = destination
        self.val = val
    def __str__(self):
        return f"Arc: {self.source} {self.destination} {self.val}"

class Arcing:
    def __init__(self, type: str, arcs: list[Arc] = []):
        self.type = type
        self.arcs = arcs
    def __str__(self):
        string = f"""Arcing: {self.type} ["""
        for i in self.arcs:
            string += f"{i} "
        return string+"]"

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token = None
        self.cursor = -1

    def next_token(self):
        self.cursor += 1
        self.current_token = self.tokens[self.cursor]
        return self.current_token

    def parsify(self):
        declaration_list = list()
        place_list = list()
        tran_list = list()
        state = 0
        while state != -1 and self.next_token().type != token.EOF:
            #place instantiation
            if self.current_token.type == token.PLACE:
                varlist = []
                while state != -1:
                    self.next_token()
                    if state == 0 and self.current_token.type == token.IDENT:
                        state = 1
                        if self.current_token.literal in place_list or self.current_token in tran_list:
                            error(f"Identifier {self.current_token.literal} already exists.")
                        place_list.append(self.current_token.literal)   
                        varlist.append(self.current_token.literal)
                    elif state == 1 and self.current_token.type == token.COMMA:
                        state = 0
                    elif state == 1 and self.current_token.type == token.SEMICOLON:
                        state = 0
                        declaration_list.append(Instantiation(token.PLACE, varlist))
                        break
                    else:
                        state = -1
            #transition instantiation
            elif self.current_token.type == token.TRAN:
                varlist = []
                while state != -1:
                    self.next_token()
                    if state == 0 and self.current_token.type == token.IDENT:
                        state = 1
                        if self.current_token.literal in place_list or self.current_token in tran_list:
                            error(f"Identifier {self.current_token.literal} already exists.")
                        tran_list.append(self.current_token.literal)   
                        varlist.append(self.current_token.literal)
                    elif state == 1 and self.current_token.type == token.COMMA:
                        state = 0
                    elif state == 1 and self.current_token.type == token.SEMICOLON:
                        state = 0
                        declaration_list.append(Instantiation(token.TRAN, varlist))
                        break
                    else:
                        state = -1
            elif self.current_token.type == token.IDENT:
                temp = self.current_token.literal
                if temp not in place_list and temp not in tran_list:
                    error(f"Identifier {temp} was not declared.")
                if state == 0 and self.next_token().type == token.DOT:
                    self.next_token()
                    if self.current_token.literal in ["amm", "cap"]:
                        type = self.current_token.literal
                        state = 1
                    elif self.current_token.literal == "in" and temp in place_list or self.current_token.literal == "out" and temp in tran_list:
                        type = "outbound"
                        state = 2
                    elif self.current_token.literal == "in" and temp in tran_list or self.current_token.literal == "out" and temp in place_list:
                        type = "inbound"
                        state = 2
                    else:
                        error("Declaration Error")
                    if state != 0 and self.next_token().type == token.ASSIGN:
                        pass
                    else:
                        state = -1
                self.next_token()
                if state == 1 and self.current_token.type == token.INT:
                    val = int(self.current_token.literal)
                    if self.next_token().type == token.SEMICOLON:
                        state = 0
                        declaration_list.append(Placefield(type, temp, val))
                    else:
                        state = -1
                elif state == 2 and self.current_token.type == token.LBRACE:
                    state = 1
                    arcs = list()
                    while state != -1:
                        self.next_token()
                        if state == 1 and self.current_token.type == token.IDENT:
                            state = 2
                            destination = self.current_token.literal
                        elif state == 2 and self.current_token.type == token.COLON:
                            state = 3
                        elif state == 3 and self.current_token.type == token.INT:
                            state = 4
                            val = int(self.current_token.literal)
                        elif state == 2 and self.current_token.type == token.COMMA:
                            state = 1
                            val = 1
                        elif state == 4 and self.current_token.type == token.COMMA:
                            state = 1
                        elif state == 2 and self.current_token.type == token.RBRACE:
                            state = 0
                            val = 1
                            break
                        elif state == 4 and self.current_token.type == token.RBRACE:
                            state = 0
                            break
                        else:
                            state = -1
                        if state == 1:
                            arcs.append(Arc(temp, destination, val))
                    if state == 0 and self.next_token().type == token.SEMICOLON:
                        arcs.append(Arc(temp, destination, val))
                        declaration_list.append(Arcing(type, list(arcs)))
                        pass
                    else:
                        state = -1
            else:
                error("Declaration Error")
        return declaration_list
    