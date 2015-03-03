import sys
import tweepy
import datetime
import urllib
import signal
import json
import os
import time

# Don't forget to install tweepy
# pip install tweepy
class TweetSerializer:
#	out = open("output.txt", "w")
	out = None
	first = True
	count = 0

	#additional variables
	tweet_counter=0

	# def start(self):
	#   self.count += 1
	#   fname = "tweets-"+str(self.count)+".json"
	#   self.out = open(fname,"w")
	#   self.out.write("[\n")
	#   self.first = True

	# def start(self,postfix=''):
	#   self.count += 1
	#   if (postfix==''):
	#   	fname = "tweets_"+str(self.count)+".json"
	#   else:
	#   	fname = "tweets_"+str(self.count)+"_"+postfix+".json"	  	
	#   self.out = open(fname,"w")
	#   self.out.write("[\n")
	#   self.first = True

	def start(self,postfix=''):
	  self.count += 1
	  if (postfix==''):
	  	# fname = subdirectory+"/tweets_"+str(self.count)+".json"
	  	fname = "tweets_"+str(self.count)+".txt"
	  else:
	  	# fname = subdirectory+"/tweets_"+str(self.count)+"_"+postfix+".json"
	  	fname = "tweets_"+str(self.count)+"_"+postfix+".txt"
	  self.out = open(fname,"w")
	  self.out.write("[\n")
	  self.first = True


	def end(self):
	  if self.out is not None:
	     self.out.write("\n]\n")
	     self.out.close()
	  self.out = None

	# def write(self,tweet):
	#   if not self.first:
	#      self.out.write(",\n")
	#   self.first = False
	#   self.out.write(json.dumps(tweet._json).encode('utf8'))

	def write(self,tweet):
	  if not self.first:
	     self.out.write(",\n")
	  self.first = False
	  tweetMessage = json.loads(json.dumps(tweet._json))['text']
	  self.out.write(tweetMessage.encode('utf8'))


	#new helper method to partition different files by specifying max number of tweets per file
	def part_by_num_tweets(self,tweet,tweet_per_file):
	 	self.tweet_counter+=1
	 	if self.tweet_counter>tweet_per_file: 
			self.end()
			self.tweet_counter=1
	 	if self.tweet_counter==1: 
	 		self.start()
		self.write(tweet)

#handling interuptions
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   # magic goes here
   exit(1)

signal.signal(signal.SIGINT, interrupt)


#Date time partition functions
xsdDatetimeFormat = "%Y-%m-%dT%H:%M:%S"
xsdDateFormat = "%Y-%m-%d"

def datetime_partition(start,end,duration):
   current = start
   while start==current or (end-current).days > 0 or ((end-current).days==0 and (end-current).seconds>0):
      yield current
      current = current + duration

def date_partition(start,end):
   return datetime_partition(start,end,datetime.timedelta(days=1))



consumer_key = "ed62uFKqU0S8K9ktav5FBPUEs"
consumer_secret = "3gos1oozXEvhFRvOW6DXxObaZUsWiSKxoBZjpSerEqYHysX5e1"

access_token = "33554204-b35KxDSTNacmyiwdCjTpbP4zryWGVkNT7dGJVf4We"
access_token_secret = "AG2PbUo6HsEi66DVyr1zvSvC4HdbfSYm7r3u8OriXCs8o"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# #Input via external query arguments to the file
# q = urllib.quote_plus(sys.argv[1])  # URL encoded query
# start = datetime.datetime.strptime(sys.argv[2],xsdDateFormat) # start date
# end = datetime.datetime.strptime(sys.argv[3],xsdDateFormat) #end date

# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"


#Input via hard-coding query values in this file
# q=urllib.quote_plus('#microsoft OR #mojang')
# q = urllib.quote_plus(sys.argv[1])  # URL encoded query
# print q
start = datetime.datetime.strptime('2015-01-19',xsdDateFormat)
end = datetime.datetime.strptime('2015-01-22',xsdDateFormat)

ts=TweetSerializer() #initialize helper class

# # chunk by number of tweets
# for tweet in tweepy.Cursor(api.search,q='#microsoft+OR+#mojang',since='2015-01-17',until='2015-01-18',).items():
# 	ts.part_by_num_tweets(tweet,1000)
# ts.end()

# chunk by number of date
for d_0 in date_partition(start,end):
	d_1=d_0
	d_1+=datetime.timedelta(days=1)
	d_0=str(d_0)[:10]
	d_1=str(d_1)[:10]
	print d_0,d_1
	ts.start(d_0)
	for tweet in tweepy.Cursor(api.search,q='#microsoft+OR+#mojang',since=d_0, until=d_1).items():
  		# ts.write(tweet)
  		# print tweet
  		ts.write(tweet)
	ts.end()
