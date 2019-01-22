# htcp-tea-parser
This is an implementation of a parser for the HTCPCP-TEA (Hypertext Coffee Pot Control Protocol-Tea Efflux Appliances) protocol.
This is part of a three part assignment implementing a working server for this protocol.

## Dependencie
This implementation is written in Python 3.7, but should be compatible with any version of Python 3, as only standard libraries are used.

## Execution instructions
Because the code is written in Python, no compilation is required to run the parser. Simply run `python3 parser.py [path-to-request]`, where
[path-to-request] is a path to a file containing a single HTCPCP-TEA request. The program will print out a response code and explanation
after parsing the request.