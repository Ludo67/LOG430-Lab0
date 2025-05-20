import unittest
from io import StringIO
import sys

def main():
    print("Hello World!")

class TestHelloWorld(unittest.TestCase):

    def test_main_prints_hello_world(self):
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout
        main()
        sys.stdout = sys.__stdout__   # Reset redirect
        self.assertEqual(captured_output.getvalue().strip(), "Hello World!")

    def test_main_does_not_print_empty_string(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertNotEqual(captured_output.getvalue().strip(), "")

if __name__ == "__main__":
    main()
