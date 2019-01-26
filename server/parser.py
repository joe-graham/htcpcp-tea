#!/usr/bin/env python

import sys

def main(filename):
    """ Start everything off, doing minor method checks.
    Optionally accepts a filename parameter to simplify unit testing.
    """
    try:
        filePointer = open(filename, "rb")
        
    except IOError:
        print("Unable to open file!")
        exit(1)

    # Line 1 is the method and URI    
    methodLine = filePointer.readline()
    methodLineSplit = methodLine.decode("UTF-8").split()
    method = methodLineSplit[0]
    uri = methodLineSplit[1]

    if method == "BREW" or method == "POST":
        parse_request(filePointer, uri)
    elif method == "GET":
        print("HTCPCP-TEA/1.0 200 OK", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
        filePointer.close()
        return
    else:
        print("HTCPCP-TEA/1.0 405 Method Not Allowed", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
        filePointer.close()
        return

def parse_request(filePointer, uri):
    """ Begin parsing headers into dict, erroring out if anything bad is found.
    Also verifies that the URI is valid, and turns away confused coffee drinkers.
    filePointer - the pointer to the open file reperesenting the HTCPCP request
    uri - The already parsed URI for the request
    """
    headerDict = dict()
    # Parse headers into a map, breaking if empty line reached (start of body)
    for line in filePointer:
        decodedLine = line.decode("UTF-8")
        # CR LF parsing
        if line[-1] != 10 or line[-2] != 13:
            print("HTCPCP-TEA/1.0 400 Bad Request", end="\r\n")
            print("", end="\r\n")
            print("", end="\r\n")
            filePointer.close()
            return
        if decodedLine == "\r\n":
            break
        # TODO: add exception handling
        lineSplit = decodedLine.split(":")
        if lineSplit[0] == "Accept-Additions":
            headerDict[lineSplit[0]] = lineSplit[1].strip().split(";")
            # lstrip removes space caused by spaces in between each addition
            for index, addition in enumerate(headerDict[lineSplit[0]]):
                headerDict[lineSplit[0]][index] = addition.lstrip()
        else:
            headerDict[lineSplit[0]] = lineSplit[1].strip()
    
    if "Content-Type" not in headerDict.keys():
        print("HTCPCP-TEA/1.0 400 Bad Request", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
        filePointer.close()
        return
    
    if headerDict["Content-Type"] == "message/coffee-pot-command":
        # If URI has two slashes, it's trying to access a tea pot, and needs a 400
        if len(uri.split("/")) == 3:
            print("HTCPCP-TEA/1.0 400 Bad Request", end="\r\n")
            filePointer.close()
            print("", end="\r\n")
            print("", end="\r\n")
            return
        else:
            print("HTCPCP-TEA/1.0 418 I'm a teapot", end="\r\n")
            print("", end="\r\n")
            print("", end="\r\n")
            filePointer.close()
            return
    
    elif headerDict["Content-Type"] == "message/teapot":
        if uri == "/":
            print("HTCPCP-TEA/1.0 300 Multiple Options", end="\r\n")
            print("Alternates: ", end='')
            for tea in ["peppermint", "black", "green", "earl-grey"]:
                print("{\"" + str(tea) + "\" {type message/teapot}}", end='')
                if tea != "earl-grey": print(",", end="\r\n")
            print("", end="\r\n")
            print("", end="\r\n")
            print("", end="\r\n")
            filePointer.close()
            return
        # If URI has only one slash, the client is trying to find a coffee pot
        elif len(uri.split("/")) == 2:
            print("HTCPCP-TEA/1.0 418 I'm a teapot", end="\r\n")
            print("", end="\r\n")
            print("", end="\r\n")
            filePointer.close()
            return
        else:
            request_handler(uri, headerDict, filePointer)

    else:
        print("HTCPCP-TEA/1.0 400 Bad Request", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
        filePointer.close()
        return

def request_handler(uri, headerDict, filePointer):
    """Handles access control to forbidden teas, verification of additions, and body validation.
    """
    if uri.split("/")[2] in ["chai", "raspberry", "oolong"]:
        print("HTCPCP-TEA/1.0 403 Forbidden", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
        filePointer.close()
        return
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
                print("HTCPCP-TEA/1.0 406 Not Acceptable", end="\r\n")
                print("", end="\r\n")
                print("", end="\r\n")
                filePointer.close()
                return
            else:
                if ((addition in dairyAdditions and dairyFound) or (addition in syrupAdditions and syrupFound) 
                or (addition in alcoholAdditions and alcoholFound) or (addition in sweetAdditions and sweetFound)):
                    print("HTCPCP-TEA/1.0 406 Not Acceptable", end="\r\n")
                    print("", end="\r\n")
                    print("", end="\r\n")
                    filePointer.close()
                    return
                else:
                    if addition in dairyAdditions: dairyFound = True
                    elif addition in syrupAdditions: syrupFound = True
                    elif addition in alcoholAdditions: alcoholFound = True
                    else: sweetFound = True
    # Check body of request to see if it has a start or stop command
    bodyRead = filePointer.readline()
    decodeBody = bodyRead.decode("UTF-8")
    if bodyRead[-1] != 10 and bodyRead[-2] != 13:
        print("HTCPCP-TEA/1.0 400 Bad Request", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
    if decodeBody != "start\r\n" and decodeBody != "stop\r\n":
        print("HTCPCP-TEA/1.0 400 Bad Request", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
    else:
        print("HTCPCP-TEA/1.0 200 OK", end="\r\n")
        print("", end="\r\n")
        print("", end="\r\n")
    filePointer.close()
    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " path-to-request")
        exit(1)
    main(sys.argv[1])
