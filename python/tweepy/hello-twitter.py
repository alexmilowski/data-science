import tweepy
import json
import urllib
#import sys

# Don't forget to install tweepy
# pip install tweepy

# Note: You must fill in your four values below from your registered application.

consumer_key = "twI3B0GuFxkAY5Y8EggYuH1MW"
consumer_secret = "MRnoOyoGOgoXAyd26Rwm2cZloVBT63MhZr5ZyvT06koxPDlIhV"

access_token = "720169710-4hstZM04S6DMKm1rr1y4Cy9TWvgTvu29LUKzbUT6"
access_token_secret = "v23joaXipB0ORm5JCEEpR8xSOEwJWkNAXidpHRlElm3hY"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class TweetSerializer:
   out = None
   first = True
   count = 0
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

serializer = TweetSerializer()
q = urllib.quote_plus("minecraft")
# try count=n
serializer.start()

for tweet in tweepy.Cursor(api.search,q=q).items(200):
    serializer.write(tweet)
serializer.end()


