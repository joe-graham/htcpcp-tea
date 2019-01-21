#!/usr/bin/env python

import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " path-to-request")
        exit(1)

    try:
        filePointer = open(sys.argv[1], "r")
        
    except IOError as e:
        print("Unable to open file!")
        exit(1)

    # Line 1 is the method and URI    
    methodLine = filePointer.readline().split()
    method = methodLine[0]
    uri = methodLine[1]

    if method == "BREW" or method == "POST":
        brewHandler(filePointer, uri)
    else:
        print("500 Internal Server Error")

    """
    elif method == "GET":
        do something
    """

def brewHandler(file_pointer, uri):
    raise NotImplementedError()

if __name__ == "__main__":
    main()
