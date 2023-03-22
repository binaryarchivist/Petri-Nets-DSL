from typing import List

from tokenizer import Token
import tokens as token


def error(message=None):
    if message:
        raise ValueError(message)
    raise ValueError("Declaration Error")


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
        self.source = source
        self.destination = destination
        self.val = val

    def __str__(self):
        return f"Arc: {self.source} {self.destination} {self.val}"


class Arcing:

    def __init__(self, type: str, arcs: List[Arc]):
        self.type = type
        self.arcs = arcs

    def __str__(self):
        string = f"Arcing: {self.type} ["
        for i in self.arcs:
            string += f"{i}, "
        return string[:-2] + "]"


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

    def next_token(self):
        self.cursor += 1
        self.current_token = self.tokens[self.cursor]
        return self.current_token

    def expect(self, token):
        temp = self.current_token.type
        self.next_token()
        if token:
            if self.current_token.type in token:
                pass
            else:
                error(f"Expected something else after {temp}.")
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

    def var_exists(self):
        if self.current_token.literal in self.var_dict[token.PLACE] or self.current_token.literal in self.var_dict[token.TRAN]:
            error(f"Identifier {self.current_token.literal} already exists.")

    def var_not_exist(self):
        if self.current_token.literal not in self.var_dict[token.PLACE] and self.current_token.literal not in \
                self.var_dict[token.TRAN]:
            error(f"Identifier {self.current_token.literal} does not exist.")

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
                        self.var_exists()
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
                self.var_not_exist()
                self.expect(token.DOT)
                self.expect(token.IDENT)

                if self.current_token.literal in ["amm", "cap"]:
                    type = self.current_token.literal
                    self.state = 1
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
                    declaration_list.append(Placefield(type, temp, val))

                # Arcing
                elif self.case(2, token.LBRACE):
                    self.state = 1
                    arclist = list()

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
                    declaration_list.append(Arcing(type, list(arclist)))

                else:
                    error("Field Declaration Error. Expected something else after '='.")
            else:
                error()
        return declaration_list

    def merge_declarations(self):
        return
