import json
import boto
from boto.s3.key import Key

class TweetSerializer:
   out = None
   first = True
   count = 0
  # c = boto.connect_s3()
  # b = c.get_bucket('cloofa-ds205')
  # k = Key(b)
 #  k.key = 'assignment2/foobar'

# k.set_contents_from_string('This is a test of S3')
   def start(self):
      self.count += 1
      fname = "tweets-"+str(self.count)+".json"
      self.out = open(fname,"w")
      self.first = True

   def end(self):
      if self.out is not None:
         self.out.close()
      self.out = None

   def write(self,tweet):
      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8'))
      self.out.write('\n')

