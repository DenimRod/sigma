import os
import sys
import urllib.request
import urllib.parse
import base64
import json

def importSignature(*args):
       #---adapt sigma_files URL taken from .odt file
    parsed = urllib.parse.urlparse(args[0])
    path = parsed.path
    netloc = parsed.netloc
        #---1 if stored on local pc, remove first / of /D:/mydir...
    if netloc == "":
        path = path[1:]
        #---2 if stored on server, add // to create //server/mydir...
    else:
        netloc = "//" + netloc
    finalPath = netloc + path

        #---load config file (used for server path)
    with open(finalPath + '/sigma_files/config.json', "r") as configFile:
        config = json.load(configFile)

    with urllib.request.urlopen(config["serverPath"] + '/signature.txt') as response:
       data = response.read()

       #---cut header of encoded file
    img_data = data[22:]

    with open(finalPath + "/sigma_files/signature.png", "wb") as newfile:
        newfile.write(base64.decodestring(img_data))
        newfile.close()

        #...optional log file
    # with open(finalPath + "/sigma_files/log.txt", 'w') as f:
    #     f.write("Success!")

    return None

def exportForm(*args):
       #---adapt sigma_files URL taken from .odt file
    parsed = urllib.parse.urlparse(args[0])
    path = parsed.path
    netloc = parsed.netloc
        #---1 if stored on local pc, remove first / of /D:/mydir...
    if netloc == "":
        path = path[1:]
        #---2 if stored on server, add // to create //server/mydir...
    else:
        netloc = "//" + netloc
    finalPath = netloc + path
        #--- load config file (used for server path)
    with open(finalPath + '/sigma_files/config.json', "r") as configFile:
        config = json.load(configFile)

    with open(finalPath + "/sigma_files/form.png", "rb") as imgfile:
        data = imgfile.read()
        encoded_string = base64.b64encode(data)

    url = config["serverPath"] + "/saveImg.php"
    values = {'type' : 'form',
                'image' : encoded_string}

    sendData = urllib.parse.urlencode(values)
    sendData = sendData.encode('ascii')
    req = urllib.request.Request(url, sendData)
    urllib.request.urlopen(req)

    #... if respose has to be read:
    # with urllib.request.urlopen(req) as response:
       # res = response.read()

    return None
