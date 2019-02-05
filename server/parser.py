#!/usr/bin/env python

import sys
import os
import json
import subprocess
import re

def main(request):
    """ Start everything off, doing minor method checks.
    Parameters:
    request - an array of strings representing the request
    Returns: response message as an array
    """

    # Line 1 is the method and URI    
    methodLine = request[0]
    methodLineSplit = methodLine.decode("UTF-8").split()
    method = methodLineSplit[0]
    uri = methodLineSplit[1]
    response = []
    # if you want to support php POST requests, change this variable to "php"
    # if you don't, change this variable to "deprecated"
    MODE = "php"

    if method == "BREW" or method == "GET":
        request.remove(request[0])
        response = parse_request(request, uri, method)
        return response
    elif method == "POST" and MODE == "deprecated":
        response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
        return response
    elif method == "POST" and MODE == "php":
        request.remove(request[0])
        response = parse_request(request, uri, method)
        return response
    else:
        response = ["HTCPCP-TEA/1.0 405 Method Not Allowed", "\r\n", "\r\n"]
        return response

def parse_request(request, uri, method):
    """ Begin parsing headers into dict, erroring out if anything bad is found.
    Also verifies that the URI is valid, and turns away confused coffee drinkers.
    request - array of strings representing request
    uri - The already parsed URI for the request
    method - The method of the request, important for different handling purposes
    Returns: response to forward to client
    """
    headerDict = dict()
    response = []
    # Parse headers into a map, breaking if empty line reached (start of body)
    while True:
        # If line doesn't include headers, syntax error
        if len(request) == 0:
            response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
            return response
        line = request[0]
        decodedLine = line.decode("UTF-8")
        # CR LF parsing
        if line[-1] != 10 or line[-2] != 13:
            response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
            return response
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
        request.remove(line)
    
    # pass on to PHP parser if URI matches
    regexp = re.match("^\/[A-Za-z]*\.php", uri)
    if regexp:
        filename = regexp.group().lstrip("/")
        response = php_handler(uri, headerDict, method, request, filename)
        return response
    # verify headers ended with a crlf
    newline = request[0]
    if line[-1] != 10 or line[-2] != 13:
        response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
        return response
    request.remove(newline)
    
    if "Content-Type" not in headerDict.keys():
        response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
        return response
    
    if headerDict["Content-Type"] == "message/coffee-pot-command":
        # If URI has two slashes, it's trying to access a tea pot, and needs a 400
        if len(uri.split("/")) == 3 and method != "GET":
            response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
            return response
        else:
            if method == "BREW":
                response = brew_handler(uri, headerDict, request)
            elif method == "GET":
                response = get_handler(uri, headerDict, request)
            return response
    
    elif headerDict["Content-Type"] == "message/teapot":
        if uri == "/":
            response = ["HTCPCP-TEA/1.0 300 Multiple Options\r\n", "Alternates: "]
            for tea in ["peppermint", "black", "green", "earl-grey"]:
                response.append("{\"" + str(tea) + "\" {type message/teapot}}")
                if tea != "earl-grey": response.append(",\r\n")
            response.append("\r\n")
            response.append("\r\n")
            return response
        # If URI has only one slash, the client is trying to find a coffee pot
        elif len(uri.split("/")) == 2 and method != "GET":
            response = ["HTCPCP-TEA/1.0 418 I'm a teapot", "\r\n", "\r\n"]
            return response
        else:
            if method == "BREW":
                response = brew_handler(uri, headerDict, request)
            elif method == "GET":
                response = get_handler(uri, headerDict, request)
            return response

    else:
        response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
        return response

def brew_handler(uri, headerDict, request):
    """Handles access control to forbidden teas, verification of additions, and body validation.
    Parameters:
    uri - URI of the request
    headerDict - dictionary containing all headers from request
    request - remaining parts of request to parse
    Returns: response to forward to client
    """
    response = []
    # only verify this if brewing tea
    if len(uri.split("/")) == 3:
        if uri.split("/")[2] in ["chai", "raspberry", "oolong"]:
            response = ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"]
            return response
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
                response = ["HTCPCP-TEA/1.0 406 Not Acceptable", "\r\n", "\r\n"]
                return response
            else:
                if ((addition in dairyAdditions and dairyFound) or (addition in syrupAdditions and syrupFound) 
                or (addition in alcoholAdditions and alcoholFound) or (addition in sweetAdditions and sweetFound)):
                    response = ["HTCPCP-TEA/1.0 406 Not Acceptable", "\r\n", "\r\n"]
                    return response
                else:
                    if addition in dairyAdditions: dairyFound = True
                    elif addition in syrupAdditions: syrupFound = True
                    elif addition in alcoholAdditions: alcoholFound = True
                    else: sweetFound = True
    # Check body of request to see if it has a start or stop command
    bodyRead = request[0]
    decodeBody = bodyRead.decode("UTF-8")
    if bodyRead[-1] != 10 and bodyRead[-2] != 13:
        response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
        return response
    if decodeBody != "start\r\n" and decodeBody != "stop\r\n":
        response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
        return response
    else:
        # Create JSON file structure
        # if tea, else coffee
        if len(uri.split("/")) == 3:
            dirName = uri.split("/")[1]
            fileName = uri.split("/")[2]
            ls = os.listdir('.')
            for item in ls:
                if item == "dirName" and os.path.isdir(item):
                    response = ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"]
                    return response
            os.mkdir("./" + dirName)
            out = {"type": "tea"}
            out["variety"] = fileName
            out["Additions"] = {}
            if "Accept-Additions" in headerDict:
                counter = 1
                for item in headerDict["Accept-Additions"]:
                    key = "addition" + str(counter)
                    out["Additions"][key] = item
                    counter += 1
            newFile = open("./" + dirName + "/" + fileName, mode="w")
            json.dump(out, newFile, indent=4)
            newFile.close()
            response = ["HTCPCP-TEA/1.0 200 OK", "\r\n", "Content-Type: message/teapot" "\r\n", "\r\n"]
        else:
            fileName = uri.split("/")[1]
            ls = os.listdir('.')
            for item in ls:
                if item == "dirName" and os.path.isdir(item):
                    response = ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"]
                    return response
            out = {"type": "coffee"}
            out["Additions"] = {}
            if "Accept-Additions" in headerDict:
                counter = 1
                for item in headerDict["Accept-Additions"]:
                    key = "addition" + str(counter)
                    out["Additions"][key] = item
                    counter += 1
            newFile = open("./" + fileName, mode="w")
            json.dump(out, newFile, indent=4)
            newFile.close()
            response = ["HTCPCP-TEA/1.0 200 OK", "\r\n", "Content-Type: message/coffee-pot-command" "\r\n", "\r\n"]
        logFile = open("./requests.log", "a")
        logFile.write("GET " + uri + " HTCPCP-TEA/1.0\n")
        logFile.close()
        return response

def get_handler(uri, headerDict, request):
    """ Handles all GET requests, including verifying that pots exist and that
    additions in GET request match acceptable additions in JSON file.
    Parameters:
    uri - URI of request
    headerDict - dictionary of headers in request
    request - remaining parts of request to parse
    Returns: response to forward to client
    """
    length = len(uri.split("/"))
    # if tea, else coffee
    if length == 3:
        pot = uri.split("/")[1]
        variety = uri.split("/")[2]
        try:
            os.stat("./" + pot + "/" + variety)
        except FileNotFoundError:
            response = ["HTCPCP-TEA/1.0 404 Not Found", "\r\n", "\r\n"]
            return response
        filePointer = open("./" + pot + "/" + variety)
        load = json.load(filePointer)
        acceptableAdditions = load["Additions"].values()
        filePointer.close()
        if headerDict["Content-Type"] != "message/teapot":
            response = ["HTCPCP-TEA/1.0 418 I'm a teapot", "\r\n", "\r\n"]
            return response
        for addition in headerDict["Accept-Additions"]:
            if addition not in acceptableAdditions:
                response = ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"]
                return response
        os.remove("./" + pot + "/" + variety)
        os.rmdir("./" + pot)
        logFile = open("./requests.log", "a")
        logFile.write("GET " + uri + " HTCPCP-TEA/1.0\n")
        logFile.close()
        response = ["HTCPCP-TEA/1.0 200 OK", "\r\n", "Content-Type: message/teapot", "\r\n", "\r\n"]
        return response
    else:
        pot = uri.split("/")[1]
        try:
            os.stat("./" + pot)
        except FileNotFoundError:
            response = ["HTCPCP-TEA/1.0 404 Not Found", "\r\n", "\r\n"]
            return response
        filePointer = open("./" + pot)
        load = json.load(filePointer)
        acceptableAdditions = load["Additions"].values()
        filePointer.close()
        if headerDict["Content-Type"] != "message/coffee-pot-command":
            response = ["HTCPCP-TEA/1.0 400 Bad Request", "\r\n", "\r\n"]
            return response
        for addition in headerDict["Accept-Additions"]:
            if addition not in acceptableAdditions:
                response = ["HTCPCP-TEA/1.0 403 Forbidden", "\r\n", "\r\n"]
                return response
        os.remove("./" + pot)
        logFile = open("./requests.log", "a")
        logFile.write("GET " + uri + " HTCPCP-TEA/1.0\n")
        logFile.close()
        response = ["HTCPCP-TEA/1.0 200 OK", "\r\n", "Content-Type: message/coffee-pot-command", "\r\n", "\r\n"]
        return response

def php_handler(uri, headerDict, method, request, filename):
    body = ""
    # Figure out location of php-cgi, since env vars aren't inherited by future subprocess call
    try:
        output = subprocess.check_output(["which", "php-cgi"])
    except subprocess.CalledProcessError:
        response = ["HTCPCP-TEA/1.0 500 Internal Server Error", "\r\n", "Content-Type: text/plain", "\r\n", "\r\n"]
        print("Unable to find php-cgi, make sure your $PATH variable contains it")
        return response
    stdout = output.decode("UTF-8")
    split = stdout.split("/")
    path = "/"
    for item in split:
        item = item.strip()
        if item != "php-cgi" and item != "":
            path += item + "/"
    path = path.rstrip("/")
    if method == "GET":
        if "?" in uri:
            queryString = uri.split("?")[1]
        else:
            queryString = ""
        envVars = {}
        envVars["QUERY_STRING"] = queryString
        envVars["SCRIPT_FILENAME"] = filename
        envVars["REDIRECT_STATUS"] = "0"
        envVars["PATH"] = path
        body = subprocess.check_output(["php-cgi", "-q", filename], env=envVars)
    # only GET or POST allowed for PHP, so else is fine
    #else:
        
    response = ["HTCPCP-TEA/1.0 200 OK", "\r\n", "Content-Type: text/plain", "\r\n", body, "\r\n"]
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " path-to-request")
        exit(1)
    try:
        filePointer = open(sys.argv[1], "rb")
        
    except IOError:
        print("Unable to open file!")
        exit(1)
    inputArray = []
    for line in filePointer:
        inputArray.append(line)
    output = main(inputArray)
    filePointer.close()
    print(output)
