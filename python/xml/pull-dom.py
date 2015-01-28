import sys
from xml.dom import pulldom
from xml import sax

parser = sax.make_parser()
parser.setFeature(sax.handler.feature_namespaces, 1)
doc = pulldom.parse(sys.argv[1],parser)

# cheating on namespace handling!
print "<summaryxmlns='http://www.w3.org/1999/xhtml'>"
for event, node in doc:
    if event == pulldom.START_ELEMENT and node.tagName == 'p':
        doc.expandNode(node)
        print(node.toxml())
print "</summary>"