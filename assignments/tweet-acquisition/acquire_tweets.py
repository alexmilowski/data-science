import sys
import os
import tweepy
import urllib
import json
import datetime
from StringIO import StringIO

import boto
from boto.s3.key import Key


class TweetSerializer(object):
    def __init__(self):
        self.out = None
        self.first = True
        self.count = 0
        self.conn = boto.connect_s3()
        self.bucket = self.conn.create_bucket('janakmayer.berkeley.storingretrieving')
        self.k = Key(self.bucket)

    def start(self):
        self.out = StringIO()
        self.count += 1
        self.out.write("[\n")
        self.first = True

    def end(self):
        if self.out is not None:
            self.out.write("\n]\n")
            self.k.key = 'twitter-assignment/' + "tweets-"+str(self.count)+".json"
            self.k.set_contents_from_string(self.out.getvalue())
            self.k.key = None
        self.out.close()

    def write(self, tweet):
        if not self.first:
            self.out.write(",\n")
        self.first = False
        self.out.write(json.dumps(tweet._json).encode('utf8'))

def datetime_partition(start,end,duration):
    current = start
    while start == current or (end-current).days > 0 or ((end-current).days == 0 and (end-current).seconds > 0):
        yield current
        current = current + duration


def date_partition(start, end):
    return datetime_partition(start, end, datetime.timedelta(days=1))


if __name__ == '__main__':
    consumer_key = os.environ['TW_CONS_KEY']
    consumer_secret = os.environ['TW_CONS_SECRET']
    access_token_key = os.environ['TW_AT_KEY']
    access_token_secret = os.environ['TW_AT_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    xsdDateFormat = "%Y-%m-%d"
    startDate = sys.argv[1]
    endDate = sys.argv[2]
    q = '#microsoft OR #mojang'  # Not enough tweets when we do AND, so doing OR instead
    recordLimit = 10000000

    start = datetime.datetime.strptime(startDate, xsdDateFormat) # start date
    end = datetime.datetime.strptime(endDate, xsdDateFormat)   # end date
    writer = TweetSerializer()
    try:
        for d in date_partition(start, end):
            query = (q
                     + " since:" + d.strftime(xsdDateFormat)
                     + " until:" + (d + datetime.timedelta(days=1)).strftime(xsdDateFormat))
            writer.start()
            for tweet in tweepy.Cursor(api.search, q=query).items(recordLimit):
                writer.write(tweet)
            writer.end()

    except KeyboardInterrupt:
        writer.end()
        print "Tweet chunking safely interrupted"
        sys.exit(0)