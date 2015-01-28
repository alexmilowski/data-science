import sys
from xml.etree import ElementTree

ElementTree.register_namespace("","http://www.w3.org/1999/xhtml")

print "<summary xmlns='http://www.w3.org/1999/xhtml'>"

doc = ElementTree.parse(sys.argv[1])
for p in doc.getroot().iter('{http://www.w3.org/1999/xhtml}p'):
   print ElementTree.tostring(p)
   
print "</summary>"
