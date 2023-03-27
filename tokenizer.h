#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "tokens.h"

typedef struct Tokenizer {
    char *input;
    int cursor;
    int read_cursor;
    char ch;
} Tokenizer;

bool is_letter(char ch) {
    return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z') || ch == '_';
}

bool is_digit(char ch) {
    return '0' <= ch && ch <= '9';
}

void read_char(Tokenizer *t) {
    if (t->read_cursor >= strlen(t->input)) {
        t->ch = 0;
    } else {
        t->ch = t->input[t->read_cursor];
    }
    t->cursor = t->read_cursor;
    t->read_cursor++;
}

Tokenizer *new_tokenizer(char *input) {
    Tokenizer *t = malloc(sizeof(Tokenizer));
    t->input = input;
    t->cursor = 0;
    t->read_cursor = 0;
    t->ch = 0;
    read_char(t);
    return t;
}

void consume_whitespace(Tokenizer *t) {
    while (t->ch == ' ' || t->ch == '\t' || t->ch == '\n' || t->ch == '\r') {
        read_char(t);
    }
}

char *read_identifier(Tokenizer *t) {
    int cursor = t->cursor;
    while (is_letter(t->ch) || is_digit(t->ch)) {
        read_char(t);
    }
    return strndup(t->input + cursor, t->cursor - cursor);
}

char *read_number(Tokenizer *t) {
    int cursor = t->cursor;
    while (is_digit(t->ch)) {
        read_char(t);
    }
    return strndup(t->input + cursor, t->cursor - cursor);
}

Token *next_token(Tokenizer *t) {
    Token *tok = malloc(sizeof(Token));
    tok->type = ILLEGAL;
    tok->literal = NULL;
    consume_whitespace(t);

    switch (t->ch) {
        case '=':
            tok->type = ASSIGN;
            break;
        case ':':
            tok->type = COLON;
            break;
        case ';':
            tok->type = SEMICOLON;
            break;
        case ',':
            tok->type = COMMA;
            break;
        case '.':
            tok->type = DOT;
            break;
        case '{':
            tok->type = LBRACE;
            break;
        case '}':
            tok->type = RBRACE;
            break;
        case '\0':
            tok->type = EOF;
            break;
        default:
            if (is_letter(t->ch)) {
                char *identifier = read_identifier(t);
                tok->literal = identifier;
                tok->type = lookup_ident(identifier);
                free(identifier);
                return tok;
            }
            if (is_digit(t->ch) && t->ch != '0') {
                char *number = read_number(t);
                tok->literal = number;
                tok->type = INT;
                free(number);
                return tok;
            }
    }

    read_char(t);
    return tok;
}

void free_tokenizer(Tokenizer* t) {
    free(t->input);
    free(t);
}

