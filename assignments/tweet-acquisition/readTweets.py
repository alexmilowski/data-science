import tweepy
import datetime
import sys
import ConfigParser
import urllib
import time
import boto
import json

#get searchterms from argument 1
searchterms = urllib.quote_plus(sys.argv[1])

#get startdate and enddate from arguments 2 and 3, compute days between and set the first day of the range
startdate = datetime.datetime.strptime(sys.argv[2],'%Y-%m-%d')
enddate = datetime.datetime.strptime(sys.argv[3],'%Y-%m-%d')
tweetDays = (enddate - startdate).days + 1
debugmode = int(sys.argv[4])
print "Retrieving tweets for " + str(sys.argv[1]) + " between " + str(startdate.date()) + " and " + str(enddate.date()) + ", " + str(tweetDays) + " days"

#read credentials file and get Twitter and AWS credentials
credentials = ConfigParser.ConfigParser()
credentials.read('/home/sgreene/Dev/ShantiGreene/credentials.py')
consumer_key = credentials.get('Twitter','consumer_key')
consumer_secret = credentials.get('Twitter','consumer_secret')
access_token = credentials.get('Twitter','access_token')
access_token_secret = credentials.get('Twitter','access_token_secret')
access_key_id = credentials.get('AWS','access_key_id')
secret_access_key = credentials.get('AWS','secret_access_key')
s3bucketname = 'datascishissncg'
#authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#authenticate to AWS
s3connection = boto.connect_s3(access_key_id, secret_access_key)
s3bucket = s3connection.get_bucket(s3bucketname)

#setup files to store tweets and words
tweetFilePath = '/home/sgreene/Dev/data/'
tweetFilePrefix = 'tweetFile.part.'
wordFilePath = '/home/sgreene/Dev/data/'
wordFilePrefix = 'wordFile.part.'

api = tweepy.API(auth)
#if the API rate limit is hit, pause until more requests can be processed
api.wait_on_rate_limit = True
totalTweets = 0
try:
    for i in range (0,tweetDays):
        tweetCount = 0
        wordCount = 0
        tweetFilename = tweetFilePath+tweetFilePrefix+str(i);
        tweetFile = open(tweetFilename,"w")
        enddate = startdate+datetime.timedelta(days=1)
        s3file = boto.s3.key.Key(s3bucket)
        s3file.key = tweetFilePrefix + str(i)
        for tweet in tweepy.Cursor(api.search, q=searchterms, since=str(startdate.date()), until=str(enddate.date()), include_entities=True).items():
            #add tweets to file for that day
            if tweet is not None: 
                tweetFile.write(json.dumps(tweet._json)+"\n")
                tweetCount += 1
                tweetWordList = tweet.text.split()
                totalTweets += 1
        i += 1
        print str(startdate.date()) + " to " + str(enddate.date()) + ", " + str(tweetCount) + " Tweets"
        tweetFile.close()
        s3file.set_contents_from_filename(tweetFilename)
        startdate = startdate+datetime.timedelta(days=1)
except KeyboardInterrupt: 
        print "search interrupted for date: "+str(startdate.date())
        print "files "+tweetFilename +" is incomplete"
        tweetFile.close()
print "Retrieval complete, " + str(totalTweets) + " Tweets.\n"


    

   