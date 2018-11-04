import unittest
import tempfile
import os
from dndcmd.main import DnDShell

tests = [
    'test_basic.txt', 'test_roll_1.txt', 'test_roll_2.txt', 'test_roll_3.txt',
    'test_diags_1.txt', 'test_diags_2.txt', 'test_diags_3.txt'
]


class CMDTest(unittest.TestCase):
    def test_main(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        for filename in tests:
            input_file_path = os.path.join(dir_path, 'inputs', filename)
            self.assertTrue(os.path.exists(input_file_path) and os.path.isfile(
                input_file_path))

            reference_file_path = os.path.join(dir_path, 'outputs', filename)
            self.assertTrue(
                os.path.exists(reference_file_path) and os.path.isfile(
                    reference_file_path))

            with self.subTest(file=filename):
                input_file = open(input_file_path, 'r')
                output_file = tempfile.TemporaryFile(mode='r+')

                shell = DnDShell(stdin=input_file, stdout=output_file)
                shell.use_rawinput = False
                shell.cmdloop()

                input_file.close()

                output_file.seek(0)
                output = output_file.readlines()
                output_file.close()

                reference_file = open(reference_file_path, 'r')
                reference = reference_file.readlines()
                reference_file.close()

                self.assertEqual(output, reference)


if __name__ == '__main__':
    unittest.main()
