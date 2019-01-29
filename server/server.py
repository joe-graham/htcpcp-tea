#!/usr/bin/env python

import sys
import socket
import threading
import parser

def main(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(5)
    while True:
        request = sock.accept()
        request_handler = threading.Thread(target=parser.main, args=(request,request))
        request_handler.start()
    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + str(sys.argv[0]) + " [ip] [port]")
        exit(1)
    main(sys.argv[1], sys.argv[2])