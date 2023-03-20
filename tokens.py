ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Identifiers
IDENT = "IDENT"  # x, y, test, temp, ...
INT = "INT"  # 123456789

# OPERATORS
ASSIGN = "="

# Delimiters
COMMA = ","
DOT = "."
SEMICOLON = ";"
LBRACE = "{"
RBRACE = "}"
COLON = ':'

# Keywords
PLACE = "PLACE"
TRAN = "TRAN"

keywords: dict = {
    "place": PLACE,
    "tran": TRAN
}


def lookup_ident(ident: str):
    if ident in keywords:
        return keywords[ident]
    return IDENT
