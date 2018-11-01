import unittest
import tempfile
from dndcmd.main import DnDShell

tests = [
    'test_basic.txt'
]


class CMDTest(unittest.TestCase):
    def test_main(self):
        for filename in tests:
            with self.subTest(file=filename):
                input_file = open('inputs/{}'.format(filename), 'r')
                output_file = tempfile.TemporaryFile(mode='r+')

                shell = DnDShell(stdin=input_file, stdout=output_file)
                shell.use_rawinput = False
                shell.cmdloop()

                input_file.close()

                output_file.seek(0)
                output = output_file.readlines()
                output_file.close()

                reference_file = open('outputs/{}'.format(filename), 'r')
                reference = reference_file.readlines()
                reference_file.close()

                self.assertEqual(output, reference)


if __name__ == '__main__':
    unittest.main()
