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


if __name__ == '__main__':
    unittest.main()
