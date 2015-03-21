#Kasane Utsumi - 3/20/2015
#analyze.py
#This code gets word frequency dictionary using tweetAnalyzer class, then plot histogram of words that are mentioned more than 1000 times

import sys
import tweepy
import datetime
import urllib
import signal
import json
import boto
from boto.s3.connection import S3Connection
import tweetserializer
import tweetanalyzer
from boto.s3.key import Key
import numpy as np
import pylab as pl
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
	print "Interrupted, closing ..."
	exit(1)

aws_access_key_id =''
aws_secret_access_key= ''
aws_bucket_name=''



conn = None
bucket = None

try:
	conn = S3Connection(aws_access_key_id,aws_secret_access_key)
	bucket = conn.get_bucket(aws_bucket_name)
except:
	print "S3 connection failed. Exiting..."
	exit()

#instantiate a utility class that retrieves tweets from S3 and creates a frequency dictionary
tweetanalyzer = tweetanalyzer.TweetAnalyzer(bucket)
wordCountDictionary = tweetanalyzer.analyze()

print(len(wordCountDictionary))

#because my vm keeps giving me "killed" error for too large dictionary 
# I have to create histogram for only words with > 1000 counts
over1000 = dict()    
for key in wordCountDictionary:
	if wordCountDictionary[key] > 1000:
		over1000[key] = wordCountDictionary[key]

print(len(over1000))

#nowfor histogram...
X = np.arange(len(over1000))
pl.bar(X,over1000.values(),width=0.2)
pl.xticks(X,over1000.keys())

ymax = max(over1000.values()) +1
pl.ylim(0,ymax)

pl.show()
