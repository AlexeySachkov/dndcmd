from dndcmd.Sema import Sema
from dndcmd.Lexer import TokenType, Token
import unittest


class TestSema(unittest.TestCase):
    def setUp(self):
        self.sema = Sema()

    def test_simple_evaluate(self):
        expr = self.sema.build_ast(
            # 2+3
            [Token(TokenType.T_NUMBER, 2, 0), Token(TokenType.T_OP, '+', 1),
             Token(TokenType.T_NUMBER, 3, 2),
             Token(TokenType.T_EOL, (), 3)])
        self.assertEqual(5, expr.evaluate())

    def test_simple_dice_roll(self):
        expr = self.sema.build_ast(
            # d6
            [Token(TokenType.T_DICE, (), 0), Token(TokenType.T_NUMBER, 6, 1),
             Token(TokenType.T_EOL, (), 2)])
        for i in range(1, 10):
            with self.subTest(i=i):
                self.assertTrue(1 <= expr.evaluate() <= 6)

    def test_print_constant(self):
        expr = self.sema.build_ast(
            # 42
            [Token(TokenType.T_NUMBER, 42, 0), Token(TokenType.T_EOL, (), 1)])
        self.assertEqual("ConstantExpr: 42", str(expr))

    def test_print_roll_dice(self):
        expr = self.sema.build_ast(
            # d20
            [Token(TokenType.T_DICE, (), 0), Token(TokenType.T_NUMBER, 20, 1),
             Token(TokenType.T_EOL, (), 3)])
        self.assertEqual("DiceRollExpr: d20", str(expr))

    def test_print_roll_dice_twice(self):
        expr = self.sema.build_ast(
            # 2d20
            [Token(TokenType.T_NUMBER, 2, 0), Token(TokenType.T_DICE, (), 1),
             Token(TokenType.T_NUMBER, 20, 2),
             Token(TokenType.T_EOL, (), 4)])
        self.assertEqual(
            "BinOpExpr: '*'\n\tConstantExpr: 2\n\tDiceRollExpr: d20",
            str(expr))

    def test_print_binop_sum(self):
        expr = self.sema.build_ast(
            # 2+3
            [Token(TokenType.T_NUMBER, 2, 0), Token(TokenType.T_OP, '+', 1),
             Token(TokenType.T_NUMBER, 3, 2), Token(TokenType.T_EOL, (), 3)])
        self.assertEqual(
            "BinOpExpr: '+'\n\tConstantExpr: 2\n\tConstantExpr: 3", str(expr))


if __name__ == '__main__':
    unittest.main()
