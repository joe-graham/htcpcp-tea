# htcp-tea-parser
This is an implementation of a server for the HTCPCP-TEA (Hypertext Coffee Pot Control Protocol-Tea Efflux Appliances) protocol.
This is part of a three part assignment implementing a working server for this protocol.

## Dependencies
This implementation is written in Python 3.7, but should be compatible with any version of Python 3, as only standard libraries are used.

## Execution instructions
Because the code is written in Python, no compilation is required to run the parser. Simply run `python3 server.py [ip] [port]`, where
[ip] is the IP address you would like the server to listen to on, and [port] is the port you would like the server to listen on. 

Requests can be sent to the server using either the curl command with
the relevant methods, or by printing the contents of a valid request,
some of which can be found in the tests/ sub-directory, directly into
netcat.