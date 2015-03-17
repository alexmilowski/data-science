import urllib2, gzip, StringIO
from xml.dom import pulldom
from xml import sax
import json
import math
import sys
import datetime

import seqs
import date_partitions as partitions

serviceURI = "http://data.pantabular.org/opennex/data/"

def fetchQuadrangle(dataset,yearMonth,resolution,sequence):
   strYearMonth = "{}-{:02d}".format(yearMonth.year,yearMonth.month)
   url = serviceURI+dataset+"/"+strYearMonth+"/"+str(resolution)+"/"+str(sequence);
   print url
   response = None
   try:
      response = urllib2.urlopen(url)
   except urllib2.HTTPError as e:
      return None
      
   html = None
   
   if response.headers.get('content-encoding', '') == 'gzip':
      data = response.read()
      compressedstream = StringIO.StringIO(data)
      gzipper = gzip.GzipFile(fileobj=compressedstream)
      html = gzipper.read()
   else:
      html = response.read()
      
   parser = sax.make_parser()
   parser.setFeature(sax.handler.feature_namespaces, 1)
   doc = pulldom.parseString(html,parser)
   
   inTable = False
   
   def textContent(parent):
      s = "";
      for n in parent.childNodes:
         if n.data != None:
            s += n.data
      return s
   
   data = []
   for event, node in doc:
       if event == pulldom.START_ELEMENT and node.tagName == 'table':
          if node.getAttribute("typeof") == "IndexedTable":
             inTable = True
       if event == pulldom.END_ELEMENT and node.tagName == 'table':
          inTable = False
       if inTable and event == pulldom.START_ELEMENT and node.tagName == 'td':
          doc.expandNode(node)
          if len(node.childNodes) > 0:
             data.append(float(textContent(node)))
             
   if len(data) == 0:
      return None
   
   return {"dataset": dataset, "yearMonth": strYearMonth, "resolution" : resolution, "sequence": sequence, "data": data }

dataset = sys.argv[1]   
resolution = int(sys.argv[2])
quad = json.loads(sys.argv[3])
start = datetime.datetime.strptime(sys.argv[4],"%Y-%m") # start month
end = datetime.datetime.strptime(sys.argv[5],"%Y-%m")   # end month
prefix = sys.argv[6]

size = resolution / 120.0


for yearMonth in partitions.month_partition(start,end):
   for seq in seqs.sequencesFromQuadrangle(size,quad):
      obj = fetchQuadrangle(dataset,yearMonth,resolution,seq)
      if obj != None:
          fileName = "{}{}-{:02d}-{}-{}.json".format(prefix,yearMonth.year,yearMonth.month,resolution,seq)
          f = open(fileName,"w")
          json.dump(obj,f)
          f.write("\n")
          f.close()

