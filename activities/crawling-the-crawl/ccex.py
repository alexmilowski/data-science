import re
import json
from urlparse import urlparse

#
from mrcc import CCJob

class Example(CCJob):
   def process_record(self, record):
      # Some header readers aren't for Web resources
      if "warc-target-uri" in record.header:
      
         uri = record.header["warc-target-uri"]
         print uri
         
         # load the payload into a string 
         payload = record.payload.read()
         
         yield uri,1
         yield "zzzz-count",1

if __name__ == '__main__':
  Example.run()