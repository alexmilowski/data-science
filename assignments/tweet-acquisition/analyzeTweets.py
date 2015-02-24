import json
import sys
import ConfigParser
import time
import boto
import codecs
import collections
import numpy as np
import matplotlib.pyplot as plt

#get startdate and enddate from arguments 2 and 3, compute days between and set the first day of the range
filePrefix = sys.argv[1]
fileParts = int(sys.argv[2]) 
debugMode = int(sys.argv[3])
tweetFilePrefix = 'tweetFile.part.'

#read credentials file and get AWS credentials
credentials = ConfigParser.ConfigParser()
credentials.read('/home/sgreene/Dev/data-science/trunk/credentials.py')
access_key_id = credentials.get('AWS','access_key_id')
secret_access_key = credentials.get('AWS','secret_access_key')
s3bucketname = 'datascishissncg'

#authenticate to AWS
s3connection = boto.connect_s3(access_key_id, secret_access_key)
s3bucket = s3connection.get_bucket(s3bucketname)

#for each file read the tweet string and split it into words
totalTweets = 0
wordCount = 0
wordList = []
for i in range (0,fileParts):
    fileName = filePrefix+str(i);  
    s3key = s3bucket.get_key(tweetFilePrefix+str(i))
    s3file = s3key.get_contents_to_filename(fileName)
    if debugMode == 1: print "Parsing file " + fileName
    with open(fileName, mode="r") as tweetFile:
        for line in tweetFile:
            tweetJSON = json.loads(line)
            tweet = tweetJSON['text']
            totalTweets += 1
            tweetWordList = tweet.split()
            for tweetWord in tweetWordList:          
                wordCount += 1
                #print tweetWord
                wordList.append(tweetWord)
    tweetFile.closed
cWordList = collections.Counter(wordList).most_common()
labels, values = zip(*cWordList)
indexes = np.arange(len(labels))
width = .5
plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5, labels, rotation=60)
plt.xlabel('Tweet Words')
plt.ylabel('Word Occurinces')
print "Found " + str(totalTweets) + " Tweets, containing " + str(wordCount) + " words, in " + str(fileParts) + " files"
plt.show()