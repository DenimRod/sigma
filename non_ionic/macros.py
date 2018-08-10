import os
import sys
import urllib.request
import urllib.parse
import base64
import json

def importSignature(*args):
       #---remove "file:///" from path, passed as argument from BASIC
    finalPath = os.path.dirname(args[0])[8:]
        #--- load config file (used for server path)
    with open(finalPath + '/sigma_files/config.json', "r") as configFile:
        config = json.load(configFile)

    with urllib.request.urlopen(config["serverPath"] + '/signature.txt') as response:
       data = response.read()

       #---cut header of encoded file
    img_data = data[22:]

    with open(finalPath + "/sigma_files/signature.png", "wb") as newfile:
        newfile.write(base64.decodestring(img_data))
        newfile.close()

        #---optional log file
    # with open(finalPath + "/sigma_files/log.txt", 'w') as f:
    #     f.write("Success!")

    return None

def exportForm(*args):
       #---remove "file:///" from path, passed as argument from BASIC
    finalPath = os.path.dirname(args[0])[8:]
        #--- load config file (used for server path)
    with open(finalPath + '/sigma_files/config.json', "r") as configFile:
        config = json.load(configFile)

    with open(finalPath + "/sigma_files/form.jpg", "rb") as imgfile:
        data = imgfile.read()
        encoded_string = base64.b64encode(data)

    url = config["serverPath"] + "/saveImg.php"
    values = {'type' : 'form',
                'image' : encoded_string}

    sendData = urllib.parse.urlencode(values)
    sendData = sendData.encode('ascii')
    req = urllib.request.Request(url, sendData)
    urllib.request.urlopen(req)
    #--- if respose has to be read: ---
    # with urllib.request.urlopen(req) as response:
       # res = response.read()

    return None
