import sys
import tweepy
import datetime
import urllib
import json
from xml.sax.saxutils import XMLGenerator
import signal

# Don't forget to install tweepy
# pip install tweepy

prefix = sys.argv[1]
minutes = datetime.timedelta(minutes=int(sys.argv[2]))
tracks = sys.argv[3:len(sys.argv)]
now = datetime.datetime.now()
nearest = now - datetime.timedelta(seconds=now.second,microseconds=now.microsecond)

# Note: You must fill in your four values below from your registered application.

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

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
      created = datetime.datetime.strptime(tweet["created_at"],"%a %b %d %H:%M:%S +0000 %Y")
      self.xml.startElementNS((self.ns,"tweet"),"tweet",{(None,"alias"):tweet["user"]["screen_name"], (None,"created"): created.strftime("%Y-%m-%dT%H-%M-%SZ")})
      self.xml.characters(tweet["text"])
      self.xml.endElementNS((self.ns,"tweet"),"tweet")
      self.xml.characters("\n")
      
   def close(self):
      if self.out != None:
         self.xml.endElementNS((self.ns,"tweets"),"tweets")
         self.xml.endDocument()
         self.out.close()
      self.xml = None
      self.out = None

# FYI: Raw JSON could be output insteam
class DataListener(tweepy.StreamListener):
   xml = None
   end = nearest + minutes
   def on_data(self, data):
      delta = self.end - datetime.datetime.now()
      if self.xml == None or delta.total_seconds() < 0:
         self.reopen()
         
      jdata = json.loads(data)

      self.xml.tweet(jdata)
       
      return True

   def on_error(self, status):
      print status
      
   def reopen(self):
      if self.xml != None:
         self.close()
      tstamp = datetime.datetime.now()
      self.end = tstamp - datetime.timedelta(seconds=tstamp.second,microseconds=tstamp.microsecond) + minutes
      name = prefix+"-"+tstamp.strftime("%Y-%m-%d-%H-%M")+".xml"
      print "Opening "+name
      
      self.xml = XMLTweets()
      self.xml.open(name)
        
   def close(self):
      self.xml.close()
      self.xml = None

listener = DataListener()
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   listener.close()
   exit(1)
   
print "Starting at: "
print nearest
    
signal.signal(signal.SIGINT, interrupt)

stream = tweepy.Stream(auth, listener)
stream.filter(track=tracks)
