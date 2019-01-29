#!/usr/bin/env python

import sys
import socket
import threading
import parser

def main(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, int(port)))
    sock.listen(5)
    while True:
        request, _ = sock.accept()
        request_handler = threading.Thread(target=handle_connection, args=(request,))
        request_handler.start()
    return

def handle_connection(socket):
    buffer = b""
    while True:
        data = socket.recv(2048)
        if data:
            buffer += data
        else: break
    print(buffer)
    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + str(sys.argv[0]) + " [ip] [port]")
        exit(1)
    main(sys.argv[1], sys.argv[2])