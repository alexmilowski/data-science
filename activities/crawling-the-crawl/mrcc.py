from __future__ import print_function

import gzip
import sys
#
import boto
import warc
#
from boto.s3.key import Key
from gzipstream import GzipStreamFile
from mrjob.job import MRJob


class CCJob(MRJob):
      
  def process_record(self, record):
    """
    Override process_record with your mapper
    """
    raise NotImplementedError('Process record needs to be customized')

  def mapper(self, _, line):
    f = None
    ## If we're on EC2 or running on a Hadoop cluster, pull files via S3
    if line.startswith("s3://"):
    
      print('Downloading ...',file=sys.stderr)
      key = None
      
      # Connect to Amazon S3 using anonymous credentials
      conn = boto.connect_s3(anon=True)
      if line.startswith("s3://"):
         pathStart = line.index('/',5)
         bucketName = line[5:pathStart]
         keyPath = line[pathStart+1:]
         print("Bucket: "+bucketName,file=sys.stderr)
         print("Key: "+keyPath,file=sys.stderr)
         bucket = conn.get_bucket(bucketName)
         key = Key(bucket,keyPath)
      else:
         print("Bucket: aws-publicdatasets",file=sys.stderr)
         print("Key: "+line,file=sys.stderr)
         bucket = conn.get_bucket("aws-publicdatasets")
         key = Key(bucket,line)
      # Start a connection to one of the WARC files
      f = warc.WARCFile(fileobj=GzipStreamFile(key))
      
    ## If we're local, use files on the local file system
    else:
      if line.startswith("file:///"):
         line = line[7:]
      print("Local: {}".format(line),file=sys.stderr)
      f = warc.WARCFile(fileobj=gzip.open(line))
    ###
    for i, record in enumerate(f):
      for key, value in self.process_record(record):
        yield key, value
      self.increment_counter('commoncrawl', 'processed_records', 1)

  def reducer(self, key, value):
    yield key, sum(value)
