from dndcmd.Sema import Sema
from dndcmd.Lexer import Token
import unittest


class TestSema(unittest.TestCase):
    def setUp(self):
        self.sema = Sema()

    def test_simple_evaluate(self):
        expr = self.sema.build_ast(
            [(Token.TOK_NUMBER, 2), (Token.TOK_OP, '+'), (Token.TOK_NUMBER, 3),
             (Token.TOK_EOL,)])
        self.assertEqual(5, expr.evaluate())

    def test_simple_dice_roll(self):
        expr = self.sema.build_ast(
            [(Token.TOK_DICE,), (Token.TOK_NUMBER, 6), (Token.TOK_EOL,)])
        for i in range(1, 10):
            with self.subTest(i=i):
                self.assertTrue(1 <= expr.evaluate() <= 6)

    def test_print_constant(self):
        expr = self.sema.build_ast([(Token.TOK_NUMBER, 42), (Token.TOK_EOL,)])
        self.assertEqual("ConstantExpr: 42", str(expr))

    def test_print_roll_dice(self):
        expr = self.sema.build_ast(
            [(Token.TOK_DICE,), (Token.TOK_NUMBER, 20), (Token.TOK_EOL,)])
        self.assertEqual("DiceRollExpr: d20", str(expr))

    def test_print_roll_dice_twice(self):
        expr = self.sema.build_ast(
            [(Token.TOK_NUMBER, 2), (Token.TOK_DICE,), (Token.TOK_NUMBER, 20),
             (Token.TOK_EOL,)])
        self.assertEqual(
            "BinOpExpr: '*'\n\tConstantExpr: 2\n\tDiceRollExpr: d20",
            str(expr))

    def test_print_binop_sum(self):
        expr = self.sema.build_ast([(Token.TOK_NUMBER, 2), (Token.TOK_OP, '+'),
                                    (Token.TOK_NUMBER, 3), (Token.TOK_EOL,)])
        self.assertEqual(
            "BinOpExpr: '+'\n\tConstantExpr: 2\n\tConstantExpr: 3", str(expr))


if __name__ == '__main__':
    unittest.main()
