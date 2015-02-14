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
           filer = open(directory +"/"+ key.name,"r")
           data = json.loads(filer.read())
           filer.close()
           #file was read into memory, now delete it to save disk space
           os.remove(directory+"/"+key.name)
           #print len(data)
           for tweet in data:
               words = tweet['text'].split(" ")
               for word in words:
                  #do some cleanup
		  
                  word=word.lower().strip()
                  #word=word.encode("utf-8").lower().strip()

                  if word == "the" or word == "a" or word=="from" or word=="to" or word=="and" or word=="for":
                       continue
                  if word in self.wordList:
                       self.wordList[word] +=1
                  else:
                       self.wordList[word] = 1  
	

  #   for key in self.wordList:
   #         print str(key) + "  " + str(self.wordList[key])
      return self.wordList
