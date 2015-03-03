import tasearchconf #API key and token
import tweepy
import datetime
import urllib
import signal
import json
import random
import time

class TweetSerializer:
   out = None
   first = True
   count = 0
   flag=True
 
   def start(self):
      if self.flag == True:
         self.count += 1
         fname = "tweets-"+str(self.count)+".txt"
         self.out = open(fname,"w")
         self.first = True
         print self.out
      else:
         exit(0)
         
   def end(self):
      if self.out is not None:
         self.out.close()
         self.out = None

   def write(self,tweet):
      if not self.first:
         self.out.write(",\n")
      self.first = False
      langtweet = tweet.lang + " " + json.dumps(tweet.text).encode('utf8')
      self.out.write(langtweet)
 
   def interrupt(self,signum, frame):
      print "Interrupted, closing ..."
      self.flag=False;
       
      

consumer_key = tasearchconf.consumer_key
consumer_secret = tasearchconf.consumer_secret
access_token = tasearchconf.access_token
access_token_secret = tasearchconf.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

objSerial= TweetSerializer()
signal.signal(signal.SIGINT, objSerial.interrupt)

tweetcount = 0
objSerial.start()
for tweet in tweepy.Cursor(api.search,
                      q='mojang microsoft since:2015-01-09 until:2015-02-05').items():
   objSerial.write(tweet)
   tweetcount +=1
   if tweetcount > 449: #put 450 tweets in each file
      objSerial.end() #end this chunk
      current = datetime.datetime.now()
      print "Taking a 15 minute break at %02d:%02d:%02d" % (current.hour, current.minute, current.second)
      time.sleep(60 * 15) #sleep for 15 minutes to avoid Tweepy error
      objSerial.start() #start a new file
      tweetcount = 0
objSerial.end() #close final file



 
 