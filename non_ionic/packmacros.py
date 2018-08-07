#Includes a py script into an LibreOffice file
import zipfile
import shutil
import os
import sys
import time

print("Delete and create directory with_macro")
shutil.rmtree("with_macro",True)
time.sleep(0.5)
os.mkdir("with_macro")

filename = "with_macro/"+sys.argv[1]
print("Open file " + sys.argv[1])
shutil.copyfile(sys.argv[1],filename)
doc = zipfile.ZipFile(filename,'a')

    # optional argument for pyfile to include
if len(sys.argv)>2:
    pyFile = sys.argv[2]
else:
    pyFile = "macro.py"

doc.write(pyFile, "Scripts/python/" + pyFile)
manifest = []
for line in doc.open('META-INF/manifest.xml'):
  if '</manifest:manifest>' in line.decode('utf-8'):
    for path in ['Scripts/','Scripts/python/','Scripts/python/'+pyFile]:
      manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="%s"/>' % path)
  manifest.append(line.decode('utf-8'))

doc.writestr('META-INF/manifest.xml', ''.join(manifest))
doc.close()
print("File created: "+filename)
