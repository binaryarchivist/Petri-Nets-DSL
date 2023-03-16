ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Identifiers
IDENT = "IDENT"  # x, y, test, temp, ...
INT = "INT"  # 123456789

# OPERATORS
ASSIGN = "="
HUIOZNAET = ':'  # sorry Vlad eu am uitat ce inseamna ;(

# Delimiters
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# Keywords
PLACE = "place"
TRAN = "tran"

keywords: dict = {
    "place": PLACE,
    "tran": TRAN
}


def lookup_ident(ident: str):
    if ident in keywords:
        return keywords[ident]
    return IDENT
