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

    def test_bad_request(self):
        out = StringIO()
        sys.stdout = out
        parser.main("tests/bad_request.txt")
        output = out.getvalue().strip()
        self.assertEqual(output, "400 Bad Request")

    def test_index(self):
        out = StringIO()
        sys.stdout = out
        parser.main("tests/index.txt")
        output = out.getvalue().strip()
        expectedOutput = "300 Multiple Options\n" \
                         "Alternates: {\"peppermint\" {type message/teapot}},\n" \
                         "{\"black\" {type message/teapot}},\n" \
                         "{\"green\" {type message/teapot}},\n" \
                         "{\"earl-grey\" {type message/teapot}}"
        self.assertEqual(output, expectedOutput)

    def test_repeated(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/accept_additions_repeated.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "406 Not Acceptable") 

    def test_two_of_a_kind(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/accept_additions_two_of_a_kind.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "406 Not Acceptable")
    
    def test_additions_1(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/accept_additions_1.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "200 OK")
    
    def test_additions_2(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/accept_additions_2.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "200 OK")
    
    def test_additions_3(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/accept_additions_3.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "200 OK")

    def test_start(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/start.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "200 OK")

    def test_stop(self):
       out = StringIO()
       sys.stdout = out
       parser.main("tests/stop.txt")
       output = out.getvalue().strip()
       self.assertEqual(output, "200 OK")

if __name__ == '__main__':    unittest.main()