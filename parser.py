#!/usr/bin/env python

import sys

def main(filename):
    try:
        filePointer = open(filename, "r")
        
    except IOError:
        print("Unable to open file!")
        exit(1)

    # Line 1 is the method and URI    
    methodLine = filePointer.readline().split()
    method = methodLine[0]
    uri = methodLine[1]

    if method == "BREW" or method == "POST":
        brewHandler(filePointer, uri)
    else:
        print("405 Method Not Allowed")
        filePointer.close()
        return

    """
    elif method == "GET":
        do something
    """

def brewHandler(file_pointer, uri):
    headerDict = dict()
    # Parse headers into a map, breaking if empty line reached (start of body)
    for line in file_pointer:
        if line == "\n":
            break
        # TODO: add exception handling
        lineSplit = line.split(":")
        headerDict[lineSplit[0]] = lineSplit[1].strip()
    
    if "Content-Type" not in headerDict.keys():
        print("400 Bad Request")
        file_pointer.close()
        return
    
    if headerDict["Content-Type"] == "message/coffee-pot-command":
        # If URI has two slashes, it's trying to access a tea pot, and needs a 400
        if len(uri.split("/")) == 3:
            print("400 Bad Request")
            file_pointer.close()
            return
        else:
            print("418 I'm a teapot")
            file_pointer.close()
            return

    print("200 OK")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " path-to-request")
        exit(1)
    main(sys.argv[1])
