#Kasane Utsumi - 3/20/2015
#retrieve.py
#This code searches tweets with hashtags "#microsoft" or "#mojang" in a date range which was passed as command arguments, and stores them into 500 raw tweet json per file which is then uploaded to S3 bucket


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
import dateutil.parser
import datetime

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)


aws_access_key_id =''
aws_secret_access_key= ''
aws_bucket_name=''

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = None
api = None

#connect to twitter api
try:
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
except:
   print "twitter connection failed. Exiting.. "
   exit()

#set search term
q = urllib.quote_plus("#microsoft OR #mojang")
#q = urllib.quote_plus(sys.argv[1])  # URL encoded query

#retrieve stard and end date from command argument
start = urllib.quote_plus(sys.argv[1])
end = urllib.quote_plus(sys.argv[2])

conn = None
bucket = None

try:
   conn = S3Connection(aws_access_key_id,aws_secret_access_key)
   bucket = conn.get_bucket(aws_bucket_name)
except:
   print "S3 connection failed. Exiting..."
   exit()



currentDate = dateutil.parser.parse(start)


while (currentDate.strftime("%Y-%m-%d") != end ):
	nextDay = currentDate + datetime.timedelta(days=1)

	#print currentDate.strftime("%Y-%m-%d") + " " + nextDay.strftime("%Y-%m-%d")
	currentDateString = currentDate.strftime("%Y-%m-%d")
	nextDateString = nextDay.strftime("%Y-%m-%d")
	
	#instantiate tweetSerializer - a utility class that takes care of chunking, and also uplaod file to S3
	tweetSerializer = tweetserializer.TweetSerializer(500,bucket,currentDateString)

	for tweet in tweepy.Cursor(api.search,q=q+" since:" + currentDateString + " until:" + nextDateString).items():
   		tweetSerializer.write(tweet)

	#if there is any open file (total number of tweets %500 was not 0), close the last file and upload to S3
	tweetSerializer.end()

	#increment time
	currentDate = currentDate + datetime.timedelta(days=1)

