import os
import sys
import urllib.request
import urllib.parse
import base64

def importSignature(*args):
    with urllib.request.urlopen('https://ordination-kutschera.at/sigma/signature.txt') as response:
       data = response.read()

       #cut header of encoded file
    img_data = data[22:]
    with open("D:/Projects/sigma/non_ionic/signature.png", "wb") as newfile:
        newfile.write(base64.decodestring(img_data))
        newfile.close()

    with open("D:/Projects/sigma/non_ionic/log.txt", 'w') as f:
        f.write("Success!")

    return None

def exportForm(*args):
    with open("D:/Projects/sigma/non_ionic/form.jpg", "rb") as imgfile:
        data = imgfile.read()
        encoded_string = base64.b64encode(data)

    url = 'https://ordination-kutschera.at/sigma/saveImg.php'
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
