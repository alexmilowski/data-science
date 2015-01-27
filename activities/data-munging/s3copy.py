import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection()
bucket = conn.get_bucket(sys.argv[1])
prefix = sys.argv[2]
for i in range(3,len(sys.argv)):
   print sys.argv[i]
   k = Key(bucket)
   k.key = prefix+"/"+sys.argv[i]
   k.set_contents_from_filename(sys.argv[i])
