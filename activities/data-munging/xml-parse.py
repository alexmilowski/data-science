import sys
from xml.etree import ElementTree

# See: https://docs.python.org/2/library/xml.etree.elementtree.html

# This will parse the document from a file.  If the handle was elsewhere, you can give it an open stream too.
doc = ElementTree.parse(sys.argv[1])

# iteration is a lot like //report in XPath
for report in doc.getroot().iter('{http://weather.milowski.com/V/APRS/}report'):
   # If the attribute isn't available, we'll get a dictionary key exception
   # so we check for its existence
   if "temperature" in report.attrib:
      print report.attrib["temperature"]