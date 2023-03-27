#ifndef TOKENS_H
#define TOKENS_H

typedef enum TokenType {
    ILLEGAL,
    EOF_,
    IDENT,
    INT,
    ASSIGN,
    COLON,
    SEMICOLON,
    COMMA,
    DOT,
    LBRACE,
    RBRACE,
    PLACE,
    TRAN
} TokenType;

typedef struct Token {
    TokenType type;
    char *literal;
} Token;

Token *new_token(TokenType type, char *literal);

int lookup_ident(char *ident) {
    if (strcmp(ident, "place") == 0) {
        return PLACE;
    }
    if (strcmp(ident, "tran") == 0) {
        return TRAN;
    }
    return IDENT;
};

#endif /* TOKENS_H */