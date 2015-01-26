import tweepy
import json;

# Don't forget to install tweepy
# pip install tweepy

consumer_key = "ed62uFKqU0S8K9ktav5FBPUEs"
consumer_secret = "3gos1oozXEvhFRvOW6DXxObaZUsWiSKxoBZjpSerEqYHysX5e1"

access_token = "33554204-b35KxDSTNacmyiwdCjTpbP4zryWGVkNT7dGJVf4We"
access_token_secret = "AG2PbUo6HsEi66DVyr1zvSvC4HdbfSYm7r3u8OriXCs8o"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for tweet in api.search(q="minecraft"):
   print tweet.text