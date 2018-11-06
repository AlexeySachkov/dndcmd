import enum


class TokenType(enum.Enum):
    T_UNKNOWN = -1
    T_EOL = 0
    T_NUMBER = 1
    T_DICE = 2
    T_PAREN = 3
    T_OP = 4

    def __str__(self):
        if self.value == TokenType.T_UNKNOWN:
            return "T_UNKNOWN"
        if self.value == TokenType.T_EOL:
            return "T_EOL"
        if self.value == TokenType.T_NUMBER:
            return "T_NUMBER"
        if self.value == TokenType.T_DICE:
            return "T_DICE"
        if self.value == TokenType.T_PAREN:
            return "T_PAREN"
        if self.value == TokenType.T_OP:
            return "T_OP"


class Token:
    def __init__(self, token_type, args, source_loc):
        self.type = token_type
        if not isinstance(args, tuple):
            self.args = (args,)
        else:
            self.args = args
        self.source_loc = source_loc

    def is_eol(self):
        return self.type == TokenType.T_EOL

    def is_number(self):
        return self.type == TokenType.T_NUMBER

    def is_dice(self):
        return self.type == TokenType.T_DICE

    def is_paren(self):
        return self.type == TokenType.T_PAREN

    def is_op(self):
        return self.type == TokenType.T_OP

    def is_unknown(self):
        return self.type == TokenType.T_UNKNOWN

    def get_arg(self):
        return self.args[0]

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.args == other.args and \
            self.source_loc == other.source_loc

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Token ({}, {}, {})".format(self.type, self.args,
                                           self.source_loc)


class Lexer:
    def __init__(self):
        self.str = ''
        self.pos = 0
        self.last_char = ''

    def tokenize(self, input_str):
        self.str = input_str
        self.pos = 0
        self.last_char = ' '

        tokens = []
        diags = []
        depth = 0
        eol = None
        while True:
            token = self.get_next_token()
            if token.is_paren():
                if token.get_arg() == '(':
                    depth = depth + 1
                else:
                    if depth == 0:
                        diags.append((token.source_loc, "Unexpected ')'"))
                    else:
                        depth = depth - 1
            tokens.append(token)
            if token.is_eol():
                eol = token
                break

        if depth > 0:
            diags.append((eol.source_loc, "Expected ')'"))

        if len(diags) != 0:
            tokens = None

        return tokens, diags

    def get_next_token(self):
        while self.pos < len(self.str) and self.str[self.pos].isspace():
            self.pos = self.pos + 1

        if self.pos >= len(self.str):
            return Token(TokenType.T_EOL, (), self.pos)

        if self.str[self.pos].isdigit():
            num_str = self.str[self.pos]
            source_loc = self.pos
            self.pos = self.pos + 1
            while self.pos < len(self.str) and self.str[self.pos].isdigit():
                num_str += self.str[self.pos]
                self.pos = self.pos + 1

            return Token(TokenType.T_NUMBER, int(num_str), source_loc)

        if self.str[self.pos] == 'd':
            source_loc = self.pos
            self.pos = self.pos + 1
            return Token(TokenType.T_DICE, (), source_loc)

        if self.str[self.pos] == '(' or self.str[self.pos] == ')':
            source_loc = self.pos
            paren = self.str[self.pos]
            self.pos = self.pos + 1
            return Token(TokenType.T_PAREN, paren, source_loc)

        if self.str[self.pos] == '+' or self.str[self.pos] == '*' or \
                self.str[self.pos] == '-' or self.str[self.pos] == '/':
            op = self.str[self.pos]
            source_loc = self.pos
            self.pos = self.pos + 1
            return Token(TokenType.T_OP, op, source_loc)

        char = self.str[self.pos]
        source_loc = self.pos
        self.pos = self.pos + 1
        return Token(TokenType.T_UNKNOWN, char, source_loc)
