import sys
import tweepy
import datetime
import urllib
import signal
import json

# Don't forget to install tweepy
# pip install tweepy
class TweetSerializer:
#	out = open("output.txt", "w")
	out = None
	first = True
	count = 0

	#additional variables
	tweet_counter=0

	def start(self):
	  self.count += 1
	  fname = "tweets-"+str(self.count)+".json"
	  self.out = open(fname,"w")
	  self.out.write("[\n")
	  self.first = True

	def end(self):
	  if self.out is not None:
	     self.out.write("\n]\n")
	     self.out.close()
	  self.out = None

	def write(self,tweet):
	  if not self.first:
	     self.out.write(",\n")
	  self.first = False
	  self.out.write(json.dumps(tweet._json).encode('utf8'))

	#new helper method to partition different files by specifying max number of tweets per file
	def part_by_num_tweets(self,tweet,tweet_per_file):
	 	self.tweet_counter+=1
	 	if self.tweet_counter>tweet_per_file: 
			ts.end()
			self.tweet_counter=1
	 	if self.tweet_counter==1: 
	 		ts.start()
		ts.write(tweet)



		
	# def part_by_day(self,days):

#handling interuptions
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   # magic goes here
   exit(1)

# signal.signal(signal.SIGINT, interrupt)


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

q = urllib.quote_plus(sys.argv[1])  # URL encoded query
start = datetime.datetime.strptime(sys.argv[2],xsdDateFormat) # start date
end = datetime.datetime.strptime(sys.argv[3],xsdDateFormat) #end date


ts=TweetSerializer() #initialize helper class

# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"
# ts.start()

# # Use new method "part_by_num_tweets" to specify no. of tweets per file
# for tweet in tweepy.Cursor(api.search,q=q).items(11):
#  	ts.part_by_num_tweets(tweet,5) 
# ts.end()  #not sure if this is what we need to handle


# Use new method "part_by_day" to specify days of tweets per file

for d_0 in date_partition(start,end):
	d_1=d_0
	d_1+=datetime.timedelta(days=1)
	ts.start()	
	for tweet in tweepy.Cursor(api.search,q=q,since=d_0, until=d_1).items(10):
		ts.part_by_num_tweets(tweet,9999)
	ts.end()

#How do you cancel this possibly long running process and still have the last chunk be syntactically valid?

#interrupt handler

#when there is a large number of tweets
