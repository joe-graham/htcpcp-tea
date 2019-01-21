#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + "path-to-request")
    exit(1)

try:
    filePointer = open(sys.argv[1], "r")
    for line in filePointer:
        print(str(line))

except IOError:
    print("Unable to open file!")
    exit(1)