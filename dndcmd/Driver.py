from dndcmd.Sema import Sema
from dndcmd.Lexer import Lexer


# TODO: add tests for Driver
class Driver:
    def __init__(self, file):
        self.file = file
        self.sema = Sema()
        self.lexer = Lexer()

    def emit_diags(self, roll_str, diags):
        for column, msg in diags:
            pointer = '^'.rjust(column + 1, ' ')
            print('Error: {}\n{}\n{}'.format(msg, roll_str, pointer),
                  file=self.file)

    def execute_roll_command(self, roll_str):
        tokens, diags = self.lexer.tokenize(roll_str)
        if tokens is None:
            self.emit_diags(roll_str, diags)
            return

        expr, diags = self.sema.build_ast(tokens)
        if expr is None:
            self.emit_diags(roll_str, diags)
        else:
            print('Result: {}'.format(expr.evaluate()), file=self.file)
