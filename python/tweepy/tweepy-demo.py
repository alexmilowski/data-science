import tweepy

# Note: You must fill in your four values below from your registered application.

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for tweet in api.search(q="minecraft"):
   print tweet.text
