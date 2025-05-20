"""A simple HelloWorld app with tests."""

import unittest
from io import StringIO
import sys

def main():
    """Main function to print Hello World."""
    print("Hello World!")  # noqa: T001

class TestHelloWorld(unittest.TestCase):
    """Unit tests for the HelloWorld script."""

    def test_main_prints_hello_world(self):
        """Test that main prints 'Hello World!'."""
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout
        main()
        sys.stdout = sys.__stdout__   # Reset redirect
        self.assertEqual(captured_output.getvalue().strip(), "Hello World!")

    def test_main_does_not_print_empty_string(self):
        """Test that main does not print an empty string."""
        captured_output = StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        self.assertNotEqual(captured_output.getvalue().strip(), "")

if __name__ == "__main__":
    main()
