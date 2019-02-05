#!/usr/bin/env python

import sys
import socket
import threading
import parser

def main(ip, port):
    """ Initializes server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, int(port)))
    sock.listen(5)
    while True:
        request, _ = sock.accept()
        request_handler = threading.Thread(target=handle_connection, args=(request,))
        request_handler.start()
    return

def handle_connection(socket):
    """ Handles every connection seen by the server. Converts bytes into parser-expected format,
    then forwards to parser, sending response back over the socket.
    socket - the socket corresponding to the client.
    """
    buffer = b""
    data = socket.recv(2048)
    buffer = data.decode("UTF-8")
    splitStr = ""
    request = []
    # convert bytes read in to request format, splitting on the new line
    # each array has each line of the request, including the /r/n, which
    # is normally stripped by .split().
    while True:
        if buffer == "":
            break
        splitStr += buffer[0]
        if buffer[0] == "\n":
            # had to open files as rb in parser, sending splitStr as
            # bytes avoids having to re-write that stuff
            request.append(bytes(splitStr, "UTF-8"))
            splitStr = ""
        buffer = buffer[1:]
    response = parser.main(request)
    for line in response:
        socket.send(bytes(line, "UTF-8"))
    socket.close()
    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + str(sys.argv[0]) + " [ip] [port]")
        exit(1)
    main(sys.argv[1], sys.argv[2])