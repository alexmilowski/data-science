import json 
import os
import boto
from boto.s3.key import Key
import string

class TweetAnalyzer:
   bucket = None
   wordList = dict()

   def __init__(self, bucket=None):
      self.bucket = bucket

   #returns words and cout as dictionary
   def analyze(self):
      #get file from s3 and store locally
      for key in self.bucket.list():
           key.get_contents_to_filename("fromS3/" + key.name)
      directory = os.getcwd() + "/fromS3"
  
      #for each file...
      for filename in os.listdir(directory):
           filer = open(directory +"/"+ filename,"r")
           data = json.loads(filer.read())
           filer.close()
           print len(data)
           for tweet in data:
               words = tweet['text'].split(" ")
               for word in words:
                  #do some cleanup
                  word=word.encode("utf-8").lower().strip()
                  if word == "the" or word == "a":
                       continue
                  if word in self.wordList:
                       self.wordList[word] +=1
                  else:
                       self.wordList[word] = 1  
	

      for key in self.wordList:
            print str(key) + "  " + str(self.wordList[key])
      return self.wordList
