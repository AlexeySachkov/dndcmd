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
        self.diags = []
        self.error = False

    def build_ast(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.diags = []
        self.error = False

        expr = self.build_expr()
        return expr, self.diags

    def build_expr(self):
        t_expr = self.build_paren_expr()
        if t_expr is None and not self.error:
            t_expr = self.build_dice_roll_expr()
            if t_expr is None and not self.error:
                t_expr = self.build_constant_expr()

        if self.error:
            return None
        elif t_expr is None:
            return None

        binop = self.build_binop_expr(t_expr)

        if binop is not None:
            return binop
        elif self.error:
            return None

        return t_expr

    def build_paren_expr(self):
        token = self.consume_token()
        if not token:
            return None

        if not token.is_paren():
            self.rollback_token()
            return None
        if token.get_arg() != '(':
            self.diag(token.source_loc, "Expected '('")
            return None

        t_expr = self.build_expr()

        token = self.consume_token()
        if not token:
            return None
        if not token.is_paren() or token.get_arg() != ')':
            self.diag(token.source_loc, "Expected ')'")
            return None

        return t_expr

    def build_dice_roll_expr(self):
        dice_or_num_token = self.consume_token()
        if not dice_or_num_token:
            return None
        if not dice_or_num_token.is_number() and \
                not dice_or_num_token.is_dice():
            self.rollback_token()
            return None

        multiplier = None
        if dice_or_num_token.is_number():
            multiplier = ConstantExpr(dice_or_num_token.get_arg())
            dice_token = self.consume_token()
            if not dice_token:
                return None
        else:
            dice_token = dice_or_num_token

        if not dice_token.is_dice():
            self.rollback_token()  # rollback dice_token
            if multiplier is not None:
                self.rollback_token()  # rollback dice_or_num_token
            return None

        dice_size_token = self.consume_token()
        if not dice_size_token:
            return None
        if not dice_size_token.is_number():
            self.diag(dice_size_token.source_loc, "Expected dice size")
            return None

        dice_roll = DiceRollExpr(dice_size_token.get_arg())

        if multiplier is None:
            return dice_roll

        return BinOpExpr(multiplier, dice_roll, '*')

    def build_constant_expr(self):
        token = self.consume_token()
        if not token:
            return None
        if not token.is_number():
            self.rollback_token()
            return None

        return ConstantExpr(token.get_arg())

    def build_binop_expr(self, lhs):
        token = self.consume_token()
        if not token:
            return None
        if not token.is_op():
            self.rollback_token()
            return None

        op = token.get_arg()

        rhs = self.build_expr()
        if rhs is None:
            self.diag(token.source_loc,
                      "Expected an expression after the '{}' operation".format(
                          op))
            return None

        next_token = self.consume_token()
        if not next_token:
            return None
        if not next_token.is_op():
            self.rollback_token()  # rollback next_token
            return BinOpExpr(lhs, rhs, op)

        next_op = next_token.get_arg()
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

    def diagnose_unknown_token(self, token):
        if token.is_unknown():
            self.diag(token.source_loc,
                      "Unexpected symbol '{}'".format(token.get_arg()))
            return True

        return False

    def diag(self, column, msg):
        self.error = True
        self.diags.append((column, msg))

    def consume_token(self):
        token = self.tokens[self.pos]
        if self.diagnose_unknown_token(token):
            return None

        self.pos = self.pos + 1
        return token

    def rollback_token(self):
        self.pos = self.pos - 1
