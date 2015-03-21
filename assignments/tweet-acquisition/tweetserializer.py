#Kasane Utsumi - 3/20/2015
#tweetserializer.py
#This is a utility class that stores x number of tweet in json format per file and then uploads each file to S3.

import json
import boto
from boto.s3.key import Key
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)




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
      
      try:
      	self.out = open(fname,"w+")
      except:
	print "Opening file failed. Exiting.. "
        exit()         

      #put wrapper for all tweet json
      self.out.write("[\n")

      self.first = True

   def end(self):

      #stop file writing, and upload file to S3
      if self.out is not None:'

         self.out.write("\n]\n")
         self.out.close()
         key = Key(self.bucket)
         key.key=self.fileName
 
         try:
	         key.set_contents_from_filename("tweets/"+self.fileName)
	 except:
                 print "Upload to s3 failed. Exiting.."
                 exit()                 

      #reset out object	
      self.out = None

   def write(self,tweet):

      #if this is first tweet in the file, create file first
      if self.tweetCount == 0:
         self.start() #initialize

      # if not first, keep writing to the opened file
      if not self.first:
         self.out.write(",\n")

      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8'))
      self.tweetCount += 1

      #if we filled the quota of specified tweet per file, call end to close the file and upload to S3
      if self.tweetCount == self.maxCount:
         self.end()
         self.tweetCount = 0

