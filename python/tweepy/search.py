import sys
import tweepy
import datetime
import urllib
import signal
from xml.sax.saxutils import XMLGenerator

# Don't forget to install tweepy
# pip install tweepy

# Note: You must fill in your four values below from your registered application.

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

prefix = sys.argv[1]
q = urllib.quote_plus(sys.argv[2])                         # URL encoded query
start = datetime.datetime.strptime(sys.argv[3],"%Y-%m-%d") # start date
end = datetime.datetime.strptime(sys.argv[4],"%Y-%m-%d")   # end date

def date_range(start,end):
   current = start
   while (end - current).days >= 0:
      yield current
      current = current + datetime.timedelta(days=1)
      

class XMLTweets():
   ns = "http://www.milowski.com/twitter"
   out = None
   xml = None
   def open(self,filename):
      self.out = open(filename,"w")
      self.xml = XMLGenerator(self.out,"utf-8")
      self.xml.startDocument()
      self.xml.startPrefixMapping("",self.ns)
      self.xml.startElementNS((self.ns,"tweets"),"tweets",{})
      self.xml.characters("\n")
      
   def tweet(self,tweet):
      self.xml.startElementNS((self.ns,"tweet"),"tweet",{(None,"alias"):tweet.user.screen_name, (None,"created"): tweet.created_at.strftime("%Y-%m-%dT%H-%M-%SZ")})
      self.xml.characters(tweet.text)
      self.xml.endElementNS((self.ns,"tweet"),"tweet")
      self.xml.characters("\n")
      
   def close(self):
      if self.out != None:
         self.xml.endElementNS((self.ns,"tweets"),"tweets")
         self.xml.endDocument()
         self.out.close()
      self.xml = None
      self.out = None
      

xmlOutput = XMLTweets()
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   xmlOutput.close()
   exit(1)

signal.signal(signal.SIGINT, interrupt)


for date in date_range(start,end):
   searchEnd = date + datetime.timedelta(days=1) 
   sdate = date.strftime("%Y-%m-%d")
   
   print "Processing {} ...".format(sdate)
   
   xmlOutput.open(prefix+"-"+sdate+".xml")
   
   # FYI: JSON is in tweet._json
   for tweet in tweepy.Cursor(api.search,q=q+" since:"+sdate+" until:"+searchEnd.strftime("%Y-%m-%d")).items():
      xmlOutput.tweet(tweet)
      
   xmlOutput.close()
      
   
