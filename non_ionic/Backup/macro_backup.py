import os
import sys
import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib
import urllib2

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )

        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)

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

if __name__ == '__main__':
    form = MultiPartForm()
    form.add_field('firstname', 'Doug')
    form.add_field('lastname', 'Hellmann')

    # Add a fake file
    form.add_file('image', 'cmd_Befehle.txt',
                  fileHandle=StringIO('Python developer and blogger.'))

    # Build the request
    request = urllib2.Request('https://ordination-kutschera.at/sigma/saveImg.php')
    request.add_header('User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)')
    body = str(form)
    request.add_header('Content-type', form.get_content_type())
    request.add_header('Content-length', len(body))
    request.add_data(body)

    print
    print 'OUTGOING DATA:'
    print request.get_data()

    print
    print 'SERVER RESPONSE:'
    print urllib2.urlopen(request).read()




    # filename = 'testimage.jpg'
    # headers = {
    #     'Content-Type': 'image/jpeg',
    #     'Content-Length': os.stat(filename).st_size,
    # }
    # imgfile = open(filename, 'rb')
    # request = urllib2.Request('https://ordination-kutschera.at/sigma/saveImg.php', imgfile.read(),
    #                           headers=headers)
    # print(request.get_data())
    # response = urllib2.urlopen(request)
    # print(response.read())

    # url = 'https://ordination-kutschera.at/sigma/saveImg.php'
    # values = {'test' : 'Success',
    #             'image' : testimage.jpg}
    #
    # data = urllib.urlencode(values)
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req)
    # print(response.read())

    # url = 'https://ordination-kutschera.at/sigma/saveImg.php?test=none'
    # req = urllib2.Request(url)
    # response = urllib2.urlopen(req)
    # print(response.read())
