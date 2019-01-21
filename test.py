import unittest
import parser
import sys
from io import StringIO

class ParserTests(unittest.TestCase):
    
    def missing_content_type(self):
        out = StringIO()
        sys.stdout = out
        parser.main("tests/missing_content_type.txt")
        output = out.getvalue().strip()
        self.assertEqual(output, "400 Bad Request")

    def test_coffee_teapot(self):
        out = StringIO()
        sys.stdout = out
        parser.main("tests/coffee_teapot.txt")
        output = out.getvalue().strip()
        self.assertEqual(output, "400 Bad Request")
    
    def test_coffee(self):
        out = StringIO()
        sys.stdout = out
        parser.main("tests/coffee.txt")
        output = out.getvalue().strip()
        self.assertEqual(output, "418 I'm a teapot")

if __name__ == '__main__':
    unittest.main()