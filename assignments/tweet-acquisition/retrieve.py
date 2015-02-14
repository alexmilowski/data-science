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



aws_access_key_id =''
aws_secret_access_key= ''
aws_bucket_name=''



# Don't forget to install tweepy
# pip install tweepy

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

q = urllib.quote_plus("#microsoft OR #mojang")
#q = urllib.quote_plus(sys.argv[1])  # URL encoded query

start = urllib.quote_plus(sys.argv[1])
end = urllib.quote_plus(sys.argv[2])
conn = S3Connection(aws_access_key_id,aws_secret_access_key)
bucket = conn.get_bucket(aws_bucket_name)
# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"
tweetSerializer = tweetserializer.TweetSerializer(500,bucket,start)
for tweet in tweepy.Cursor(api.search,q=q+" since:" + start + " until:" + end).items():
   # FYI: JSON is in tweet._json
   tweetSerializer.write(tweet)
tweetSerializer.end()

