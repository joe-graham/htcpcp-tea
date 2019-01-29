import unittest
import parser
import sys
from io import StringIO
import os

class ParserTests(unittest.TestCase):
   def read_file(self, filename):
      try:
         filePointer = open(filename, "rb")
        
      except IOError:
         print("Unable to open file!")
         exit(1)
      inputArray = []
      for line in filePointer:
         inputArray.append(line)
      filePointer.close()
      return inputArray
      
   def test_missing_content_type(self):
      request = self.read_file("tests/missing_content_type.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

   def test_coffee_teapot(self):
      request = self.read_file("tests/coffee_teapot.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

   def test_teapot_coffee(self):
      request = self.read_file("tests/teapot_coffee.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 418 I'm a teapot", "\r\n", "\r\n"])
    
   def test_coffee(self):
      request = self.read_file("tests/coffee.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0")

   def test_bad_request(self):
      request = self.read_file("tests/bad_request.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

   def test_index(self):
      request = self.read_file("tests/index.txt")
      output = parser.main(request)
      expectedOutput = ["HTCPCP-TEA/1.0 300 Multiple Options\r\n",
                        "Alternates: ", "{\"peppermint\" {type message/teapot}}", ",\r\n",
                        "{\"black\" {type message/teapot}}", ",\r\n",
                        "{\"green\" {type message/teapot}}", ",\r\n",
                        "{\"earl-grey\" {type message/teapot}}", "\r\n", "\r\n"]
      self.assertEqual(output, expectedOutput)

   def test_repeated(self):
      request = self.read_file("tests/accept_additions_repeated.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 406 Not Acceptable", "\r\n", "\r\n"]) 

   def test_two_of_a_kind(self):
      request = self.read_file("tests/accept_additions_two_of_a_kind.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 406 Not Acceptable", "\r\n", "\r\n"])
    
   def test_additions(self):
      request = self.read_file("tests/accept_additions_1.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0/peppermint")
      os.rmdir("./pot-0")

      request = self.read_file("tests/accept_additions_2.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0/earl-grey")
      os.rmdir("./pot-0")
    
      request = self.read_file("tests/accept_additions_3.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-1/peppermint")
      os.rmdir("./pot-1")

      request = self.read_file("tests/coffee_additions_1.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0")

      request = self.read_file("tests/coffee_additions_2.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-1")
    
      request = self.read_file("tests/coffee_additions_3.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0")


   def test_start(self):
      request = self.read_file("tests/start.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0/peppermint")
      os.rmdir("./pot-0")

   def test_stop(self):
      request = self.read_file("tests/stop.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 200 OK", "\r\n", "\r\n"])
      os.remove("./pot-0/peppermint")
      os.rmdir("./pot-0")

   def test_forbidden(self):
      request = self.read_file("tests/forbidden_1.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"])

      request = self.read_file("tests/forbidden_2.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"])

      request = self.read_file("tests/forbidden_3.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"])

   def test_body(self):
      request = self.read_file("tests/invalid_body.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

   def test_post(self):
      request = self.read_file("tests/post.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

   def test_invalid_content_type(self):
      request = self.read_file("tests/invalid_content_type.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

   def test_bad_newline(self):
      request = self.read_file("tests/malformed_newlines.txt")
      output = parser.main(request)
      self.assertEqual(output, ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"])

if __name__ == '__main__':    unittest.main()