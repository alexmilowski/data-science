import json
import boto
from boto.s3.key import Key




class TweetSerializer:
   out = None
   first = True
   tweetCount = 0
   maxCount = 0
   fileCount = 0
   bucket = None
   fileName = None
   fileDate = ""

   def __init__(self, maxCount=10,bucket=None,fileDate = ""):
      self.maxCount = maxCount
      self.bucket = bucket
      self.fileDate = fileDate

   def start(self):
      self.fileCount += 1
      self.fileName = "tweets-"+self.fileDate+ "-" +str(self.fileCount)+".json"
      fname= "tweets/"+ self.fileName
      self.out = open(fname,"w+")
      self.out.write("[\n")
      self.first = True

   def end(self):
      if self.out is not None:
         self.out.write("\n]\n")
         self.out.close()
         key = Key(self.bucket)
         key.key=self.fileName
         key.set_contents_from_filename("tweets/"+self.fileName)
      self.out = None

   def write(self,tweet):
      if self.tweetCount == 0:
         self.start() #initialize
      if not self.first:
         self.out.write(",\n")
      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8'))
      self.tweetCount += 1
      if self.tweetCount == self.maxCount:
         self.end()
         self.tweetCount = 0


