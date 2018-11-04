from dndcmd.Lexer import Token
import random


class Expr:
    def evaluate(self):
        raise RuntimeError()

    def __str__(self):
        pass


class DiceRollExpr(Expr):
    def __init__(self, dice_size):
        self.dice_size = dice_size

    def evaluate(self):
        return random.randint(1, self.dice_size)

    def __str__(self):
        return "DiceRollExpr: d{}".format(str(self.dice_size))


class ConstantExpr(Expr):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return "ConstantExpr: {}".format(str(self.value))


class BinOpExpr(Expr):
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self):
        if self.op == '+':
            return self.lhs.evaluate() + self.rhs.evaluate()
        if self.op == '-':
            return self.lhs.evaluate() - self.rhs.evaluate()
        if self.op == '*':
            return self.lhs.evaluate() * self.rhs.evaluate()
        if self.op == '/':
            return self.lhs.evaluate() / self.rhs.evaluate()

    def __str__(self):
        return "BinOpExpr: '{}'\n\t{}\n\t{}".format(self.op, self.lhs,
                                                    self.rhs)


class Sema:
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.expr = None

    def build_ast(self, tokens):
        self.tokens = tokens
        self.pos = 0
        return self.build_expr()

    def build_expr(self):
        t_expr = self.build_paren_expr()
        if t_expr is None:
            t_expr = self.build_dice_roll_expr()
            if t_expr is None:
                t_expr = self.build_constant_expr()

        if t_expr is None:
            raise RuntimeError()

        binop = self.build_binop_expr(t_expr)

        if binop is not None:
            return binop

        return t_expr

    def build_paren_expr(self):
        if self.cur_tok() != Token.TOK_PAREN:
            return None
        if self.cur_tok_arg() != '(':
            raise RuntimeError()

        self.next_tok()
        t_expr = self.build_expr()

        if self.cur_tok() != Token.TOK_PAREN:
            raise RuntimeError()
        if self.cur_tok_arg() != ')':
            raise RuntimeError()

        self.next_tok()
        return t_expr

    def build_dice_roll_expr(self):
        if self.cur_tok() != Token.TOK_NUMBER and \
                self.cur_tok() != Token.TOK_DICE:
            return None

        multiplier = None
        if self.cur_tok() == Token.TOK_NUMBER:
            multiplier = ConstantExpr(self.cur_tok_arg())
            self.next_tok()

        if self.cur_tok() != Token.TOK_DICE:
            self.rollback_tok()
            return None

        self.next_tok()

        if self.cur_tok() != Token.TOK_NUMBER:
            raise RuntimeError()

        dice_roll = DiceRollExpr(self.cur_tok_arg())
        self.next_tok()

        if multiplier is None:
            return dice_roll

        return BinOpExpr(multiplier, dice_roll, '*')

    def build_constant_expr(self):
        if self.cur_tok() != Token.TOK_NUMBER:
            return None

        constant = ConstantExpr(self.cur_tok_arg())
        self.next_tok()
        return constant

    def build_binop_expr(self, lhs):
        if self.cur_tok() != Token.TOK_OP:
            return None

        op = self.cur_tok_arg()
        self.next_tok()

        rhs = self.build_expr()
        if self.cur_tok() != Token.TOK_OP:
            return BinOpExpr(lhs, rhs, op)

        next_op = self.cur_tok_arg()
        if self.get_precedence(op) >= self.get_precedence(next_op):
            binop = BinOpExpr(lhs, rhs, op)
            return self.build_binop_expr(binop)

        return BinOpExpr(lhs, self.build_binop_expr(rhs), op)

    def get_precedence(self, op):
        if op == '+' or op == '-':
            return 10
        if op == '*' or op == '/':
            return 40

        return -1

    def cur_tok(self):
        return self.tokens[self.pos][0]

    def cur_tok_arg(self):
        return self.tokens[self.pos][1]

    def next_tok(self):
        self.pos = self.pos + 1
        return self.cur_tok()

    def rollback_tok(self):
        self.pos = self.pos - 1
