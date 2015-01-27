import sys
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection()
for uri in sys.argv[1:]:
   m = re.match(r"s3://([\w\-]+)/(.*)",uri)
   if m:
      bucket = conn.get_bucket(m.group(1))
      k = Key(bucket)
      k.key = m.group(2)
      print k.get_contents_as_string()
