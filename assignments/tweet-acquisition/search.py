import sys
import tweepy
import datetime
import urllib
import signal
import json
import tweet_serializer
import partitions
import tweet_auth


bucket = tweet_serializer.TweetSerializer()

def interrupt(signum, frame):
   print "Interrupted, closing ..."
   bucket.end()
   exit(1)

signal.signal(signal.SIGINT, interrupt)
datefmt = "%Y-%m-%d"

auth = tweepy.OAuthHandler(tweet_auth.consumer_key, tweet_auth.consumer_secret)
auth.set_access_token(tweet_auth.access_token, tweet_auth.access_token_secret)
api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

querybase = urllib.quote_plus(sys.argv[1])
start = datetime.datetime.strptime(sys.argv[2], datefmt)
end = datetime.datetime.strptime(sys.argv[3], datefmt)

for dt in partitions.date_partition(start, end):
    start_date = dt.strftime(datefmt)
    end_date = dt + datetime.timedelta(hours=24)
    end_date = end_date.strftime(datefmt)
    query = querybase + " since:" + start_date + " until:" +  end_date 

    bucket.start()

    for tweet in tweepy.Cursor(api.search,q=query).items():
        bucket.write(tweet)

    bucket.end()




