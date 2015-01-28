import tweepy
import json

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

# try count=n
public_tweets = api.user_timeline("alexmilowski")
for tweet in public_tweets:
    print tweet.text
