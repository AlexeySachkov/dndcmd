import unittest
from dndcmd.Lexer import Lexer, TokenType, Token


class LexerTest(unittest.TestCase):
    def setUp(self):
        self.lex = Lexer()

    def helper(self, input, ref_tokens, ref_diags=None):
        no_tokens = False
        if ref_diags is None:
            ref_diags = []
        else:
            no_tokens = True

        tokens, diags = self.lex.tokenize(input)
        if no_tokens:
            self.assertIsNone(tokens)
        else:
            self.assertListEqual(ref_tokens, tokens)

        self.assertEqual(ref_diags, diags)

    def test_eol(self):
        self.helper('', [Token(TokenType.T_EOL, (), 0)])

    def test_eol_with_spaces(self):
        self.helper('     ', [Token(TokenType.T_EOL, (), 5)])

    def test_number(self):
        self.helper('234', [Token(TokenType.T_NUMBER, 234, 0),
                            Token(TokenType.T_EOL, (), 3)])

    def test_dice(self):
        self.helper('d', [Token(TokenType.T_DICE, (), 0),
                          Token(TokenType.T_EOL, (), 1)])

    def test_parens(self):
        self.helper('()', [Token(TokenType.T_PAREN, '(', 0),
                           Token(TokenType.T_PAREN, ')', 1),
                           Token(TokenType.T_EOL, (), 2)])

    def test_op(self):
        self.helper('+*-/',
                    [Token(TokenType.T_OP, '+', 0),
                     Token(TokenType.T_OP, '*', 1),
                     Token(TokenType.T_OP, '-', 2),
                     Token(TokenType.T_OP, '/', 3),
                     Token(TokenType.T_EOL, (), 4)])

    def test_simple(self):
        self.helper('2d6 + 4',
                    [Token(TokenType.T_NUMBER, 2, 0),
                     Token(TokenType.T_DICE, (), 1),
                     Token(TokenType.T_NUMBER, 6, 2),
                     Token(TokenType.T_OP, '+', 4),
                     Token(TokenType.T_NUMBER, 4, 6),
                     Token(TokenType.T_EOL, (), 7)])

    def test_unknown(self):
        self.helper('???', [Token(TokenType.T_UNKNOWN, '?', 0),
                            Token(TokenType.T_UNKNOWN, '?', 1),
                            Token(TokenType.T_UNKNOWN, '?', 2),
                            Token(TokenType.T_EOL, (), 3)])

    def test_missed_parens(self):
        self.helper('(', None, [(1, "Expected ')'")])

    def test_missed_parens_2(self):
        self.helper(')', None, [(0, "Unexpected ')'")])


if __name__ == '__main__':
    unittest.main()
