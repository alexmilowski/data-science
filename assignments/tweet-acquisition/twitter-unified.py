import sys
import tweepy
import datetime
import urllib
import signal
import json
import os
import re
import string
from boto.s3.connection import S3Connection




# creds
credFile = open("creds.txt", 'r')
#twitter creds
consumer_key = credFile.readline().rstrip()
consumer_secret = credFile.readline().rstrip()

access_token = credFile.readline().rstrip()
access_token_secret = credFile.readline().rstrip()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#aws creds
access_key_id = credFile.readline().rstrip()
secret_access_key = credFile.readline().rstrip()

awsConn = S3Connection(access_key_id, secret_access_key)

credFile.close()




def interrupt(signum, frame):
   print "Interrupted, closing ..."
   fname.close()
   exit(1)


signal.signal(signal.SIGINT, interrupt)


#A better way
#To chunk the tweets by date, pick a range of dates,
#open a file named after the date, put all the tweets from that date in it
#one per line, close the file, and repeat

#Start date
start = datetime.date(2015,2,01)
#how many days
duration = 7
#list of search terms
searchTerms = ["#mojang","#microsoft"]
#open bucket in case we want to save directly to S3
twitterBucket = awsConn.get_bucket("chris.dailey.twitter.data")
#loop through the number of days to define an offset from the start date
for i in range(0, duration):
    print "Opening file...\n"
    #name the file to include the date plus the current duration offset
    fname = "tweets-" + str(start+datetime.timedelta(days=i)) + ".txt"
    localFile = open(fname, 'w')
    for term in searchTerms:
        #build a string for twitter that includes since: start+offset and until+offset+1
        q = urllib.quote_plus(term) + " since:" + str(start + datetime.timedelta(days=i)) + " until:" + str(start + datetime.timedelta(days=i+1))
        #print to help debug
        print "\t"+q
        #write to the file
        for tweet in tweepy.Cursor(api.search, q=q, lang="en").items(1000):
            localFile.write((tweet.text + "\n").encode('utf8'))
    print "...Closing file.\n"
    #close the file and start over
    localFile.close()
    

#define an empty dictionary to hold the results
#keys will be the words, values will be the counts
counts = {}

#list all the files in the folder...
for fileName in os.listdir("."):
    #...but keep only the ones matching the format I defined
    if (re.search("^tweets-.*-.*-.*\.txt", fileName)):
        file = open(fileName)
        #print to help debug
        print "Checking " + fileName + "..."
        #lower the text and split the lines into words
        for s in file.read().lower().split():
            #strip the punctuation
            word = s.translate(string.maketrans("",""), string.punctuation)
            #if counts doesn't have the key it's the first time we're seeing the word
            if (word not in counts):
                counts[word] = 1
            #otherwise increment by 1
            else:
                counts[word] = counts[word] + 1
        file.close()


outFile = open("results.txt",'w')
#just roll through the dictionary and make a csv for easy parsing 
#(the lack of punctuation makes this easy)
for k, v in counts.iteritems():
    outFile.write(k + ", " + str(v) + "\n")
outFile.close();
