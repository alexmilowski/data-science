import tweepy
import authtoken

api = tweepy.API(authtoken.auth)

for tweet in api.search(q="minecraft"):
   print tweet.text
