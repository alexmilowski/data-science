import tweepy

# Don't forget to install tweepy
# pip install tweepy

consumer_key = "...";
consumer_secret = "...";

access_token = "...";
access_token_secret = "...";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
