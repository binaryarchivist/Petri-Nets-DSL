from tokenizer import Token
import tokens as token

def error(message=None):
    if error:
        raise ValueError(message)
    raise ValueError("Declaration Error")

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
        self.var_dict = {
            token.PLACE : list(),
            token.TRAN : list()
        }
        self.state = 0

    def next_token(self):
        self.cursor += 1
        self.current_token = self.tokens[self.cursor]
        return self.current_token

    def expect(self, state=None, token=None):
        self.next_token()
        if state:
            if self.state == state:
                pass
            else:
                error()
        if token:
            if self.current_token.type in token:
                pass
            else:
                error()
        return True

    def case(self, state=None, token=None):
        if state:
            if self.state == state:
                pass
            else:
                return False
        if token:
            if self.current_token.type in token:
                pass
            else:
                return False
        return True

    def var_exists(self, var, raise_error=False):
        if var in self.var_dict[token.PLACE] or var in self.var_dict[token.TRAN]:
            if raise_error:
                error(f"Identifier {var} already exists.")

    def var_not_exist(self, var, raise_error=False):
        if var not in self.var_dict[token.PLACE] and var not in self.var_dict[token.TRAN]:
            if raise_error:
                error(f"Identifier {var} does not exist.")

    def parsify(self):
        declaration_list = list()
        self.state = 0
        while self.next_token().type != token.EOF:

            if self.case(0, [token.PLACE, token.TRAN]):
                type = self.current_token.type
                varlist = list()

                while self.next_token():

                    if self.case(0, token.IDENT):
                        self.state = 1
                        self.var_exists(self.current_token.literal, True)  
                        varlist.append(self.current_token.literal)

                    elif self.case(1, token.COMMA):
                        self.state = 0

                    elif self.case(1, token.SEMICOLON):
                        self.state = 0
                        declaration_list.append(Instantiation(type, varlist))
                        self.var_dict[type] += varlist
                        break

                    else:
                        error("Place Instantiation Error")

            elif self.case(0, token.IDENT):

                temp = self.current_token.literal
                self.var_not_exist(temp, True)
                self.expect(0, token.DOT)
                self.next_token()

                if self.current_token.literal in ["amm", "cap"]:
                    type = self.current_token.literal
                    self.state = 1
                elif self.current_token.literal == "in" and temp in self.var_dict[token.PLACE] or self.current_token.literal == "out" and temp in self.var_dict[token.TRAN]:
                    type = "outbound"
                    self.state = 2
                elif self.current_token.literal == "in" and temp in self.var_dict[token.TRAN] or self.current_token.literal == "out" and temp in self.var_dict[token.PLACE]:
                    type = "inbound"
                    self.state = 2
                else:
                    error(f"Field Declaration Error. Expected something else after {temp} instead of {self.current_token.literal}.")
                    
                self.expect(token = token.ASSIGN)
                self.next_token()

                #Placefield
                if self.case(1, token.INT):
                    val = int(self.current_token.literal)
                    self.expect(token=token.SEMICOLON)
                    self.state = 0
                    declaration_list.append(Placefield(type, temp, val))

                #Arcing
                elif self.case(2, token.LBRACE):
                    self.state = 1
                    arcs = list()
                    while self.next_token():
                        val = 1

                        if self.case(1, token.IDENT):
                            self.var_not_exist(self.current_token.literal, True)
                            self.state = 2
                            destination = self.current_token.literal
                            val = 1

                        elif self.case(2, token.COLON):
                            self.state = 3
                            self.expect(token = token.INT)
                            val = int(self.current_token.literal)
                            
                        elif self.case(3, token.COMMA):
                            self.state = 1

                        elif self.case(3, token.RBRACE):
                            self.state = 0
                            break

                        else:
                            error()

                        if self.state == 1:
                            arcs.append(Arc(temp, destination, val))
                            val = None

                    if self.state == 0 and self.next_token().type == token.SEMICOLON:
                        arcs.append(Arc(temp, destination, val))
                        declaration_list.append(Arcing(type, list(arcs)))
                        pass
                else:
                    error("Field Declaration Error. Expected something else after '='.")
            else:
                error()
        return declaration_list
    