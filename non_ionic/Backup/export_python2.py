import urllib
import urllib2
import base64
#import StringIO

with open("form.jpg", "rb") as imgfile:
    data = imgfile.read()
    encoded_string = data.encode("base64")

url = 'https://ordination-kutschera.at/sigma/saveImg.php'
values = {'type' : 'form',
            'image' : encoded_string}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
print(response.read())
