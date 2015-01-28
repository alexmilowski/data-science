import sys
from xml import sax

class OutputNames(sax.ContentHandler):
   def startElementNS(self, name, qname,attrs):
      print "{{{}}}{}".format(name[0],name[1])
      
parser = sax.make_parser()
parser.setFeature(sax.handler.feature_namespaces, 1)

parser.setContentHandler(OutputNames())

parser.parse(sys.argv[1])