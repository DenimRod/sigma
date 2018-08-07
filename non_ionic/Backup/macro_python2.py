import os
import sys
# import urllib
# import urllib2
# import base64
# import StringIO

def PythonVersion(*args):
    """Prints the Python version into the current document"""
    #get the doc from the scripting context which is made available to all scripts
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    #check whether there's already an opened document. Otherwise, create a new one
    if not hasattr(model, "Text"):
        model = desktop.loadComponentFromURL(
            "private:factory/swriter","_blank", 0, () )
            #get the XText interface
    text = model.Text
    #create an XTextRange at the end of the document
    tRange = text.End
    #and set the string
    tRange.String = "The Python version is %s.%s.%s" % sys.version_info[:3] + " and the executable path is " + sys.executable

    return None

# def export(*args):
#     with open("form.jpeg", "rb") as imgfile:
#         data = imgfile.read()
#         encoded_string = data.encode("base64")
#
#     url = 'https://ordination-kutschera.at/sigma/saveImg.php'
#     values = {'type' : 'form',
#                 'image' : encoded_string}
#
#     data = urllib.urlencode(values)
#     req = urllib2.Request(url, data)
#     response = urllib2.urlopen(req)
#     print(response.read())
