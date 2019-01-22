#!/usr/bin/env python

import sys

def main(filename):
    """ Start everything off, doing minor method checks.
    Optionally accepts a filename parameter to simplify unit testing.
    """
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
        brew_handler(filePointer, uri)
    elif method == "GET":
        print("200 OK")
        return
    else:
        print("405 Method Not Allowed")
        filePointer.close()
        return

def brew_handler(filePointer, uri):
    """ Begin parsing headers, erroring out if anything bad is found.
    filePointer - the pointer to the open file reperesenting the HTCPCP request
    uri - The already parsed URI for the request
    """
    headerDict = dict()
    # Parse headers into a map, breaking if empty line reached (start of body)
    for line in filePointer:
        if line == "\n":
            break
        # TODO: add exception handling
        lineSplit = line.split(":")
        if lineSplit[0] == "Accept-Additions":
            headerDict[lineSplit[0]] = lineSplit[1].strip().split(";")
            # lstrip removes space caused by spaces in between each addition
            for index, addition in enumerate(headerDict[lineSplit[0]]):
                headerDict[lineSplit[0]][index] = addition.lstrip()
        else:
            headerDict[lineSplit[0]] = lineSplit[1].strip()
    
    if "Content-Type" not in headerDict.keys():
        print("400 Bad Request")
        filePointer.close()
        return
    
    if headerDict["Content-Type"] == "message/coffee-pot-command":
        # If URI has two slashes, it's trying to access a tea pot, and needs a 400
        if len(uri.split("/")) == 3:
            print("400 Bad Request")
            filePointer.close()
            return
        else:
            print("418 I'm a teapot")
            filePointer.close()
            return
    
    elif headerDict["Content-Type"] == "message/teapot":
        if uri == "/":
            print("300 Multiple Options")
            print("Alternates: ", end='')
            for tea in ["peppermint", "black", "green", "earl-grey"]:
                print("{\"" + str(tea) + "\" {type message/teapot}}", end='')
                if tea != "earl-grey": print(",")
            print()
            filePointer.close()
        else:
            tea_handler(uri, headerDict, filePointer)

    else:
        print("400 Bad Request")
        filePointer.close()
        return

def tea_handler(uri, headerDict, filePointer):
    if "Accept-Additions" in headerDict:
        dairyAdditions = ["Cream", "Half-and-half", "Whole-milk", "Part-skim", "Skim", "Non-Dairy"]
        dairyFound = False
        syrupAdditions = ["Vanilla", "Almond", "Raspberry", "Chocolate"]
        syrupFound = False
        alcoholAdditions = ["Whisky", "Rum", "Kahlua", "Aquavit"]
        alcoholFound = False
        sweetAdditions = ["Sugar", "Xylitol", "Stevia"]
        sweetFound = False
        # Iterate over each addition, testing to see if the addition is allowed, and if we've already seen it
        for addition in headerDict["Accept-Additions"]:
            if (addition not in dairyAdditions and addition not in syrupAdditions and
            addition not in alcoholAdditions and addition not in sweetAdditions):
                print("406 Not Acceptable")
                filePointer.close()
                return
            else:
                if ((addition in dairyAdditions and dairyFound) or (addition in syrupAdditions and syrupFound) 
                or (addition in alcoholAdditions and alcoholFound) or (addition in sweetAdditions and sweetFound)):
                    print("406 Not Acceptable")
                    filePointer.close()
                    return
                else:
                    if addition in dairyAdditions: dairyFound = True
                    elif addition in syrupAdditions: syrupFound = True
                    elif addition in alcoholAdditions: alcoholFound = True
                    else: sweetFound = True
    # Check body of request to see if it has a start or stop command
    body = filePointer.readline()
    if body != "start" and body != "stop":
        print("400 Bad Request")
    else:
        print("200 OK")
    filePointer.close()
    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " path-to-request")
        exit(1)
    main(sys.argv[1])
