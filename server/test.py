import unittest
import parser
import sys
from io import StringIO

class ParserTests(unittest.TestCase):
    
   def missing_content_type(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/missing_content_type.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 400 Bad Request\r\n\r\n\r\n")

   def test_coffee_teapot(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/coffee_teapot.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 400 Bad Request\r\n\r\n\r\n")

   def test_teapot_coffee(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/teapot_coffee.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 418 I'm a teapot\r\n\r\n\r\n")
    
   def test_coffee(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/coffee.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 418 I'm a teapot\r\n\r\n\r\n")

   def test_bad_request(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/bad_request.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 400 Bad Request\r\n\r\n\r\n")

   def test_index(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/index.txt")
      output = out.getvalue()
      expectedOutput = "HTCPCP-TEA/1.0 300 Multiple Options\r\n" \
                        "Alternates: {\"peppermint\" {type message/teapot}},\r\n" \
                        "{\"black\" {type message/teapot}},\r\n" \
                        "{\"green\" {type message/teapot}},\r\n" \
                        "{\"earl-grey\" {type message/teapot}}\r\n" \
                        "\r\n\r\n"
      self.assertEqual(output, expectedOutput)

   def test_repeated(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/accept_additions_repeated.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 406 Not Acceptable\r\n\r\n\r\n") 

   def test_two_of_a_kind(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/accept_additions_two_of_a_kind.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 406 Not Acceptable\r\n\r\n\r\n")
    
   def test_additions(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/accept_additions_1.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 200 OK\r\n\r\n\r\n")

      out = StringIO()
      sys.stdout = out
      parser.main("tests/accept_additions_2.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 200 OK\r\n\r\n\r\n")
    
      out = StringIO()
      sys.stdout = out
      parser.main("tests/accept_additions_3.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 200 OK\r\n\r\n\r\n")

   def test_start(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/start.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 200 OK\r\n\r\n\r\n")

   def test_stop(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/stop.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 200 OK\r\n\r\n\r\n")

   def test_forbidden(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/forbidden_1.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 403 Forbidden\r\n\r\n\r\n")

      out = StringIO()
      sys.stdout = out
      parser.main("tests/forbidden_2.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 403 Forbidden\r\n\r\n\r\n")

      out = StringIO()
      sys.stdout = out
      parser.main("tests/forbidden_3.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 403 Forbidden\r\n\r\n\r\n")

   def test_body(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/invalid_body.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 400 Bad Request\r\n\r\n\r\n")

   def test_post(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/post.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 200 OK\r\n\r\n\r\n")

   def test_invalid_content_type(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/invalid_content_type.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 400 Bad Request\r\n\r\n\r\n")

   def test_bad_newline(self):
      out = StringIO()
      sys.stdout = out
      parser.main("tests/malformed_newlines.txt")
      output = out.getvalue()
      self.assertEqual(output, "HTCPCP-TEA/1.0 400 Bad Request\r\n\r\n\r\n")

if __name__ == '__main__':    unittest.main()