import sys
import tweepy
import datetime
import urllib
import signal
import authtoken
import serializer

api = tweepy.API(auth_handler=authtoken.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

query_string = ""

if len(sys.argv) > 1:
	query_string += sys.argv[1]

# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"

if len(sys.argv) > 2:
	query_string += " since:" + sys.argv[2]

if len(sys.argv) > 3:
	query_string += " until:" + sys.argv[3]

print query_string

tweet_serializer = serializer.TweetSerializer(2)

for tweet in tweepy.Cursor(api.search,q=query_string).items(10):
	# FYI: JSON is in tweet._json
	tweet_serializer.write(tweet)

tweet_serializer.close_file()
