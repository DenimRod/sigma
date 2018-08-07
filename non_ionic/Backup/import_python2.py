import os
import sys
import urllib
import urllib2
from base64 import decodestring
import StringIO

# def insertSignature(*args):
#     #get the doc from the scripting context which is made available to all scripts
#     desktop = XSCRIPTCONTEXT.getDesktop()
#     model = desktop.getCurrentComponent()
#     #check whether there's already an opened document. Otherwise, create a new one
#     if not hasattr(model, "Text"):
#         model = desktop.loadComponentFromURL(
#             "private:factory/swriter","_blank", 0, () )
#             #get the XText interface
#     text = model.Text
#     #create an XTextRange at the end of the document
#     tRange = text.End
#     #and set the string
#     tRange.String = "The Python version is %s.%s.%s" % sys.version_info[:3] + " and the executable path is " + sys.executable
#
#     return None

with open("D:\Projects\sigma-py\log.txt", 'w') as f:
    f.write(sys.version)


url = 'https://ordination-kutschera.at/sigma/signature.txt'
req = urllib2.Request(url)
response = urllib2.urlopen(req)
data = response.read()
    #cut header of encoded file
img_data = data[22:]
with open("signature.png", "wb") as newfile:
    newfile.write(decodestring(img_data))
    newfile.close()
