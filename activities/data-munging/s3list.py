import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection()
bucket = conn.get_bucket(sys.argv[1])

subset = sys.argv[2] if len(sys.argv)>2 else ""

for key in bucket.list(prefix=subset):
   print key.key

