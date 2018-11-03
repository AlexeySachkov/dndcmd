import enum


class Token(enum.Enum):
    TOK_UNKNOWN = -1
    TOK_EOL = 0
    TOK_NUMBER = 1
    TOK_DICE = 2
    TOK_PAREN = 3
    TOK_OP = 4


class Lexer:
    def __init__(self):
        self.str = ''
        self.pos = 0
        self.last_char = ''
        self.cur_token = Token.TOK_UNKNOWN

    def tokenize(self, input_str):
        self.str = input_str
        self.pos = 0
        self.last_char = ' '

        tokens = []
        while True:
            tok = self.get_next_token()
            tokens.append(tok)
            if tok[0] == Token.TOK_EOL:
                break

        return tokens

    def get_next_token(self):
        self.cur_token = self.get_token()
        return self.cur_token

    def get_token(self):
        while self.pos < len(self.str) and self.str[self.pos].isspace():
            self.pos = self.pos + 1

        if self.pos >= len(self.str):
            return Token.TOK_EOL,

        if self.str[self.pos].isdigit():
            num_str = self.str[self.pos]
            self.pos = self.pos + 1
            while self.pos < len(self.str) and self.str[self.pos].isdigit():
                num_str += self.str[self.pos]
                self.pos = self.pos + 1

            return Token.TOK_NUMBER, int(num_str)

        if self.str[self.pos] == 'd':
            self.pos = self.pos + 1
            return Token.TOK_DICE,

        if self.str[self.pos] == '(' or self.str[self.pos] == ')':
            paren = self.str[self.pos]
            self.pos = self.pos + 1
            return Token.TOK_PAREN, paren

        if self.str[self.pos] == '+' or self.str[self.pos] == '*' or \
                self.str[self.pos] == '-' or self.str[self.pos] == '/':
            op = self.str[self.pos]
            self.pos = self.pos + 1
            return Token.TOK_OP, op

        char = self.str[self.pos]
        self.pos = self.pos + 1
        return Token.TOK_UNKNOWN, char
