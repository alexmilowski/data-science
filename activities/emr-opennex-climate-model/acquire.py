import urllib2, gzip, StringIO
from xml.dom import pulldom
from xml import sax
import json
import math
import sys
import datetime

import seqs
import date_partitions as partitions

# Service URI for data set
serviceURI = "http://data.pantabular.org/opennex/data/"

# Fetches a sequence number data give the facets

def fetchQuadrangle(dataset,yearMonth,resolution,sequence):

   # Format a URI
   strYearMonth = "{}-{:02d}".format(yearMonth.year,yearMonth.month)
   url = serviceURI+dataset+"/"+strYearMonth+"/"+str(resolution)+"/"+str(sequence);
   print url
   
   # Open an HTTP Request
   response = None
   try:
      response = urllib2.urlopen(url)
   except urllib2.HTTPError as e:
      return None
      
   html = None
   
   # Unpack the response
   if response.headers.get('content-encoding', '') == 'gzip':
      data = response.read()
      compressedstream = StringIO.StringIO(data)
      gzipper = gzip.GzipFile(fileobj=compressedstream)
      html = gzipper.read()
   else:
      html = response.read()
      
   # Parse the markup
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
   
   # Process the markup as a stream and detect the table of data
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
   
   # Return the sequence number data object
   return {"dataset": dataset, "yearMonth": strYearMonth, "resolution" : resolution, "sequence": sequence, "data": data }

# The data set name
dataset = sys.argv[1]   

# The resolution in 1/120 degree counts
resolution = int(sys.argv[2])

# The quadrangle to cover
quad = json.loads(sys.argv[3])

# The start and end year/month
start = datetime.datetime.strptime(sys.argv[4],"%Y-%m") # start month
end = datetime.datetime.strptime(sys.argv[5],"%Y-%m")   # end month

# The prefix for the output files
prefix = sys.argv[6]

# Compute the degree size of the quadrangles
size = resolution / 120.0

# Iterate over the months
for yearMonth in partitions.month_partition(start,end):

   # Iterate over the sequence numbers for the quadrangle
   for seq in seqs.sequencesFromQuadrangle(size,quad):
   
      # Fetch a sequence number's data
      obj = fetchQuadrangle(dataset,yearMonth,resolution,seq)
      if obj != None:
      
          # Serialize the data as JSON
          fileName = "{}{}-{:02d}-{}-{}.json".format(prefix,yearMonth.year,yearMonth.month,resolution,seq)
          f = open(fileName,"w")
          json.dump(obj,f)
          f.write("\n")
          f.close()

