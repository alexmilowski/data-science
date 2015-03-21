#Kasane Utsumi - 3/20/2015
#tweetanalyzer.py
#This is a utility class that downloads chunked tweet files from S3, and creates a dictionary with word as a key and frequency of occurrence as a value. 

import json 
import os
import boto
from boto.s3.key import Key
import string
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)


class TweetAnalyzer:
   bucket = None
   wordList = dict()

   def __init__(self, bucket=None):
      self.bucket = bucket

   #returns words and cout as dictionary
   def analyze(self):

      #get file from s3 and store locally; assumption here is that tweet files are all that are stored in the specified bucket location. Thus, we can just iterate through all of the files in there. 
      for key in self.bucket.list():

	   try:
	           key.get_contents_to_filename("fromS3/" + key.name)
	   except:
                   print "file retieval failed with" + key.name
                   continue #just go to next file
                   
      
           directory = os.getcwd() + "/fromS3"

           filer = None
      
           try:
	           filer = open(directory +"/"+ key.name,"r")
           except:
	           print "could not open file" + key.name
  	 	   continue
 
           data = json.loads(filer.read())

           #file was read into memory, now delete it to save disk space
           filer.close()
           os.remove(directory+"/"+key.name)

           for tweet in data:
               words = tweet['text'].split(" ")
               for word in words:

                  #do some cleanup		  
                  word=word.lower().strip()
                  #word=word.encode("utf-8").lower().strip()
	
                  #excludes these helping words which we are not interested, and also exclude URLs 
                  if word == "the" or word == "a" or word=="from" or word=="to" or word=="and" or word=="for" or word.startswith("http://") or word.startswith("https://"):
                       continue
                  if word in self.wordList:
                       self.wordList[word] +=1
                  else:
                       self.wordList[word] = 1  
	

  #   for key in self.wordList:
   #         print str(key) + "  " + str(self.wordList[key])
      return self.wordList