import sys
import tweepy
import datetime
import urllib
import signal
import json
import authtoken

api = tweepy.API(auth_handler=authtoken.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

q = urllib.quote_plus(sys.argv[1])  # URL encoded query

# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"
for tweet in tweepy.Cursor(api.search,q=q).items(200):
   # FYI: JSON is in tweet._json
   print tweet._json
