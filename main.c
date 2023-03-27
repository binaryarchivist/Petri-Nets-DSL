#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tokenizer.h"

typedef struct TestTokenizer {
    Tokenizer *tokenizer;
} TestTokenizer;

TestTokenizer *new_test_tokenizer(char *input) {
    TestTokenizer *tt = (TestTokenizer *) malloc(sizeof(TestTokenizer));
    tt->tokenizer = new_tokenizer(input);
    return tt;
}

void free_test_tokenizer(TestTokenizer *tt) {
    free_tokenizer(tt->tokenizer);
    free(tt);
}

Token **test_next_token(TestTokenizer *tt) {
    Token **tokens = (Token **) malloc(sizeof(Token *) * 100);
    Token *tok = next_token(tt->tokenizer);
    int i = 0;

    while (tok->type != EOF_) {
        tokens[i++] = tok;
        tok = next_token(tt->tokenizer);
    }

    tokens[i++] = tok;
    tokens[i] = NULL;

    return tokens;
}

int main() {
    char *input = "place p1, p2; place p3, p4; tran t1, t2; p1.amm = 3; p1.cap = 4; p2.cap = 4; t1.out = {p1 : 2, p2 : 3}; p1.out = {t2 : 5}; p2.in = {t1, t2}; t2.in = {p3, p4};";
    TestTokenizer *tt = new_test_tokenizer(input);

    Token **tokens = test_next_token(tt);
    printf("Tokens:\n");
    for (int i = 0; tokens[i] != NULL; i++) {
        printf("Type: %d, Literal: %s\n", tokens[i]->type, tokens[i]->literal);
        free(tokens[i]->literal);
        free(tokens[i]);
    }
    free(tokens);

    free_test_tokenizer(tt);

    return 0;
}
