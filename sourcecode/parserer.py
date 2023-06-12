from typing import List
from tokenizer import Token
import tokens as token

def error(message=None):
    if message:
        raise ValueError(message)
    raise ValueError("Declaration Error")

#These are all the types of declarations used in the DSL
#They are broken down to simple attributes that should be contained in the syntax

class Instantiation:

    def __init__(self, type: str, varlist: List[str]):
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
        self.source: str = source
        self.destination: str = destination
        self.val: int = val

    def __str__(self):
        return f"Arc: {self.source} {self.destination} {self.val}"


class Arcing:

    def __init__(self, type: str, arcs: List[Arc]):
        self.type: str = type
        self.arcs: list[Arc] = arcs

    def __str__(self):
        string = f"Arcing: {self.type} ["
        for i in self.arcs:
            string += f"{i}, "
        return string[:-2] + "]"


#Parser class - Constructor takes in the list of tokens produced by the Tokenizer

class Parser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token = None
        self.cursor = -1
        self.state = 0
        self.var_dict = {
            token.PLACE: list(),
            token.TRAN: list()
        }

# The next_token method iterates to the next token given and assigns the class attribute current_token to it.

    def next_token(self):
        self.cursor += 1
        self.current_token = self.tokens[self.cursor]
        return self.current_token

# "expect" function - takes in a token type string.
# Raises error if the current token type does not match.

    def expect(self, token):
        temp = self.current_token.type
        if self.next_token().type in token:
            pass
        else:
            error(f"Expected something else after {temp}.")

# "case" function - takes in a state variable and a token type string.
# Returns True or False whether they match with the current state and token type.

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

# "var_exists" function - checks if the literal on the current token is in the variable dictionary lists.
#  Raises error if the variable already exists.

    def var_exists(self):
        if self.current_token.literal in self.var_dict[token.PLACE] or self.current_token.literal in self.var_dict[token.TRAN]:
            error(f"Identifier {self.current_token.literal} already exists.")

# "var_not_exist" function - checks if the literal on the current token is not in the variable dictionary lists.
# Raises error if the variable doesn't exist.

    def var_not_exist(self):
        if self.current_token.literal not in self.var_dict[token.PLACE] and self.current_token.literal not in \
                self.var_dict[token.TRAN]:
            error(f"Identifier {self.current_token.literal} does not exist.")

# "parsify" function - main function of the Parser class.
# Iterates through the token list, checks for correct continuity of the tokens.
# Uses expect function for mandatory tokens and uses case function for multiple cases possibility.
# The self.state variable acts as a finite automaton state control variable,
# it can also be viewed as a filter for identifying which token should be next.

    def parsify(self):
        self.declaration_list: list = list()
        self.state = 0
        while self.next_token().type != token.EOF:

            # Every declaration begins with a certain type of token, depending on which type,
            # we know the course of tokens that must follow.

            #Instantiation Section

            if self.case(0, [token.PLACE, token.TRAN]):
                type = self.current_token.type
                varlist = list()

                #Loops through the tokens until a SEMICOLON is found, stores all variables in a list.

                while self.next_token():

                    if self.case(0, token.IDENT):
                        self.state = 1
                        self.var_exists()
                        varlist.append(self.current_token.literal)

                    elif self.case(1, token.COMMA):
                        self.state = 0

                    elif self.case(1, token.SEMICOLON):
                        self.state = 0
                        self.declaration_list.append(Instantiation(type, varlist))
                        self.var_dict[type] += varlist
                        break

                    else:
                        error("Instantiation Error")

            # Placefield/Arcing Section

            elif self.case(0, token.IDENT):

                temp = self.current_token.literal
                self.var_not_exist()
                self.expect(token.DOT)
                self.expect(token.IDENT)

                # Placefield identifier

                if self.current_token.literal in ["amm", "cap"]:
                    type = self.current_token.literal
                    self.state = 1

                # Type of Arcing identifier

                elif self.current_token.literal == "in" and temp in self.var_dict[token.PLACE]:
                    type = "outbound"
                    self.state = 2
                    swap = True
                elif self.current_token.literal == "out" and temp in self.var_dict[token.TRAN]:
                    type = "outbound"
                    self.state = 2
                    swap = False
                elif self.current_token.literal == "in" and temp in self.var_dict[token.TRAN]:
                    type = "inbound"
                    self.state = 2
                    swap = True
                elif self.current_token.literal == "out" and temp in self.var_dict[token.PLACE]:
                    type = "inbound"
                    self.state = 2
                    swap = False

                else:
                    error(
                        f"Field Declaration Error. Expected something else after {temp} instead of {self.current_token.literal}.")

                self.expect(token.ASSIGN)
                self.next_token()

                # Placefield

                if self.case(1, token.INT):
                    val = int(self.current_token.literal)
                    self.expect(token.SEMICOLON)
                    self.state = 0
                    self.declaration_list.append(Placefield(type, temp, val))

                # Arcing

                elif self.case(2, token.LBRACE):
                    self.state = 1
                    arclist = list()

                    # Loops through the tokens until RBRACE is found.
                    # Stores variables and weights in a arclist.
                    # Sets weight to default value 1.

                    while self.next_token():

                        if self.case(1, token.IDENT):
                            self.var_not_exist()
                            self.state = 2
                            destination = self.current_token.literal
                            val = 1

                        elif self.case(2, token.COLON):
                            self.expect(token.INT)
                            val = int(self.current_token.literal)

                        elif self.case(2, [token.COMMA, token.RBRACE]):
                            self.state = 1
                            if swap:
                                arclist.append(Arc(destination, temp, val))
                            else:
                                arclist.append(Arc(temp, destination, val))
                            if self.case(token=token.RBRACE):
                                self.state = 0
                                break

                        else:
                            error("Arcing Declaration Error.")

                    self.expect(token.SEMICOLON)
                    self.declaration_list.append(Arcing(type, list(arclist)))

                else:
                    error("Field Declaration Error. Expected something else after '='.")
            else:
                error()
        return self.declaration_list

    def build_AST(self):
        place = dict()
        places = list()
        places_amm = 0
        tran = dict()
        trans = list()
        trans_amm = 0
        arc_in = []
        arc_out = []
        for declaration in self.declaration_list:
            
            if declaration.type == token.PLACE:
                for var in declaration.varlist:
                    temp_dict = {
                        "var": var,
                        "ID": places_amm,
                        "amm": 0,
                        "cap": float("inf")
                    }
                    place[var] = temp_dict
                    places.append(var)
                    places_amm += 1

            elif declaration.type == token.TRAN:
                for var in declaration.varlist:
                    temp_dict = {
                        "var": var,
                        "ID": trans_amm
                    }
                    tran[var] = temp_dict
                    trans.append(var)
                    trans_amm += 1

            elif type(declaration) == Placefield:
                place[declaration.var][declaration.type] = declaration.val

            elif declaration.type == "inbound":
                for arc in declaration.arcs:
                    temp_source = {
                        "var": arc.source,
                        "ID": place[arc.source]["ID"]
                    }
                    temp_destination = {
                        "var": arc.destination,
                        "ID": tran[arc.destination]["ID"]
                    }
                    temp_dict = {
                        "source": temp_source,
                        "destination": temp_destination,
                        "weight": arc.val
                    }
                    arc_in.append(temp_dict)
            
            elif declaration.type == "outbound":
                for arc in declaration.arcs:
                    temp_source = {
                        "var": arc.source,
                        "ID": tran[arc.source]["ID"]
                    }
                    temp_destination = {
                        "var": arc.destination,
                        "ID": place[arc.destination]["ID"]
                    }
                    temp_dict = {
                        "source": temp_source,
                        "destination": temp_destination,
                        "weight": arc.val
                    }
                    arc_out.append(temp_dict)

        return {
            "places": places,
            "place": place,
            "trans": trans,
            "tran": tran,
            "arc_in": arc_in,
            "arc_out": arc_out,
        }