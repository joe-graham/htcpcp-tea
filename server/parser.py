#!/usr/bin/env python

import sys

def main(filename, out):
    """ Start everything off, doing minor method checks.
    Optionally accepts a filename parameter to simplify unit testing.
    """
    if out == sys.stdout:
        try:
            filePointer = open(filename, "rb")
        
        except IOError:
            print("Unable to open file!")
            exit(1)
    
    # this is usually a socket used by the webserver
    else: 
        filePointer = out

    # Line 1 is the method and URI    
    methodLine = filePointer.readline()
    methodLineSplit = methodLine.decode("UTF-8").split()
    method = methodLineSplit[0]
    uri = methodLineSplit[1]

    if method == "BREW" or method == "POST":
        parse_request(filePointer, uri, out)
    elif method == "GET":
        out.write("HTCPCP-TEA/1.0 200 OK")
        out.write("\r\n")
        out.write("\r\n")
        filePointer.close()
        return
    else:
        out.write("HTCPCP-TEA/1.0 405 Method Not Allowed")
        out.write("\r\n")
        out.write("\r\n")
        filePointer.close()
        return

def parse_request(filePointer, uri, out):
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
            out.write("HTCPCP-TEA/1.0 400 Bad Request")
            out.write("\r\n")
            out.write("\r\n")
            filePointer.close()
            return
        if decodedLine == "\r\n":
            break
        lineSplit = decodedLine.split(":")
        if lineSplit[0] == "Accept-Additions":
            headerDict[lineSplit[0]] = lineSplit[1].strip().split(";")
            # lstrip removes space caused by spaces in between each addition
            for index, addition in enumerate(headerDict[lineSplit[0]]):
                headerDict[lineSplit[0]][index] = addition.lstrip()
        else:
            headerDict[lineSplit[0]] = lineSplit[1].strip()
    
    if "Content-Type" not in headerDict.keys():
        out.write("HTCPCP-TEA/1.0 400 Bad Request")
        out.write("\r\n")
        out.write("\r\n")
        filePointer.close()
        return
    
    if headerDict["Content-Type"] == "message/coffee-pot-command":
        # If URI has two slashes, it's trying to access a tea pot, and needs a 400
        if len(uri.split("/")) == 3:
            out.write("HTCPCP-TEA/1.0 400 Bad Request")
            filePointer.close()
            out.write("\r\n")
            out.write("\r\n")
            return
        else:
            out.write("HTCPCP-TEA/1.0 418 I'm a teapot")
            out.write("\r\n")
            out.write("\r\n")
            filePointer.close()
            return
    
    elif headerDict["Content-Type"] == "message/teapot":
        if uri == "/":
            out.write("HTCPCP-TEA/1.0 300 Multiple Options\r\n")
            out.write("Alternates: ")
            for tea in ["peppermint", "black", "green", "earl-grey"]:
                out.write("{\"" + str(tea) + "\" {type message/teapot}}")
                if tea != "earl-grey": out.write(",\r\n")
            out.write("\r\n")
            out.write("\r\n")
            filePointer.close()
            return
        # If URI has only one slash, the client is trying to find a coffee pot
        elif len(uri.split("/")) == 2:
            out.write("HTCPCP-TEA/1.0 418 I'm a teapot")
            out.write("\r\n")
            out.write("\r\n")
            filePointer.close()
            return
        else:
            request_handler(uri, headerDict, filePointer, out)

    else:
        out.write("HTCPCP-TEA/1.0 400 Bad Request")
        out.write("\r\n")
        out.write("\r\n")
        filePointer.close()
        return

def request_handler(uri, headerDict, filePointer, out):
    """Handles access control to forbidden teas, verification of additions, and body validation.
    """
    if uri.split("/")[2] in ["chai", "raspberry", "oolong"]:
        out.write("HTCPCP-TEA/1.0 403 Forbidden")
        out.write("\r\n")
        out.write("\r\n")
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
                out.write("HTCPCP-TEA/1.0 406 Not Acceptable")
                out.write("\r\n")
                out.write("\r\n")
                filePointer.close()
                return
            else:
                if ((addition in dairyAdditions and dairyFound) or (addition in syrupAdditions and syrupFound) 
                or (addition in alcoholAdditions and alcoholFound) or (addition in sweetAdditions and sweetFound)):
                    out.write("HTCPCP-TEA/1.0 406 Not Acceptable")
                    out.write("\r\n")
                    out.write("\r\n")
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
        out.write("HTCPCP-TEA/1.0 400 Bad Request")
        out.write("\r\n")
        out.write("\r\n")
    if decodeBody != "start\r\n" and decodeBody != "stop\r\n":
        out.write("HTCPCP-TEA/1.0 400 Bad Request")
        out.write("\r\n")
        out.write("\r\n")
    else:
        out.write("HTCPCP-TEA/1.0 200 OK")
        out.write("\r\n")
        out.write("\r\n")
    filePointer.close()
    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " path-to-request")
        exit(1)
    main(sys.argv[1], sys.stdout)
