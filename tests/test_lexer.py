import unittest
from dndcmd.Lexer import Lexer, Token


class LexerTest(unittest.TestCase):
    def setUp(self):
        self.lex = Lexer()

    def helper(self, input, reference):
        tokens = self.lex.tokenize(input)
        self.assertEqual(reference, tokens)

    def test_eol(self):
        self.helper('', [(Token.TOK_EOL,)])

    def test_eol_with_spaces(self):
        self.helper('     ', [(Token.TOK_EOL,)])

    def test_number(self):
        self.helper('234', [(Token.TOK_NUMBER, 234), (Token.TOK_EOL,)])

    def test_dice(self):
        self.helper('d', [(Token.TOK_DICE,), (Token.TOK_EOL,)])

    def test_parens(self):
        self.helper('()', [(Token.TOK_PAREN, '('), (Token.TOK_PAREN, ')'),
                           (Token.TOK_EOL,)])

    def test_op(self):
        self.helper('+*-/', [(Token.TOK_OP, '+'), (Token.TOK_OP, '*'),
                             (Token.TOK_OP, '-'), (Token.TOK_OP, '/'),
                             (Token.TOK_EOL,)])

    def test_simple(self):
        self.helper('2d6 + 4', [(Token.TOK_NUMBER, 2), (Token.TOK_DICE,),
                                (Token.TOK_NUMBER, 6), (Token.TOK_OP, '+'),
                                (Token.TOK_NUMBER, 4), (Token.TOK_EOL,)])

    def test_unknown(self):
        self.helper('???', [(Token.TOK_UNKNOWN, '?'), (Token.TOK_UNKNOWN, '?'),
                            (Token.TOK_UNKNOWN, '?'), (Token.TOK_EOL,)])


if __name__ == '__main__':
    unittest.main()

