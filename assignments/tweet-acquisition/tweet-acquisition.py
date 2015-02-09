#! /usr/bin/env python

__author__ = 'tkunicki'


import datetime
import json
import string
import sys
import tweepy
import urllib


class TweetSerializer:

    out = None
    chunk_count = 0
    tweet_count = 0
    write_method = None

    def __init__(self, basename, chunk_size=1000):
        self.basename = basename
        self.chunk_size = chunk_size
        self.write_method = self.__write_first

    def write(self, tweet):
        self.write_method(tweet)

    def close(self):
        if self.out:
            self.out.write("\n]\n")
            self.out.close()
        self.out = None
        self.write_method = self.__write_first

    def __chunk(self):
        self.close()

    def __write(self, tweet):
        self.out.write(json.dumps(tweet._json).encode('utf8'))
        self.tweet_count += 1

    def __write_first(self, tweet):
        path = "%s.%s.json" % (self.basename, self.chunk_count)
        self.chunk_count += 1
        self.out = open(path, "w")
        self.out.write("[\n")
        self.__write(tweet)
        self.write_method = self.__write_delimited

    def __write_delimited(self, tweet):
        self.out.write(",\n")
        self.__write(tweet)
        if self.tweet_count % self.chunk_size == 0:
            self.__chunk()


def datetime_partition(start, end, duration):
    current = start
    while start == current or (end - current).days > 0 or ((end - current).days == 0 and (end - current).seconds > 0):
        yield current
        current = current + duration


def date_partition(start, end):
    return datetime_partition(start, end, datetime.timedelta(days=1))


def tweepy_auth(credentials, user=False):
    if user:
        auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        return auth
    else:
        return tweepy.AppAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])


def tweepy_api(auth):
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def tweepy_query(api, q, since=None, until=None):
    return tweepy.Cursor(api.search, q=urllib.quote_plus(q), since=since, until=until, count=100).items()


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except IOError:
        print "Error loading %s" % path
    except ValueError:
        print "Error parsing %s" % path


def load_credentials(path="credentials.json"):
    return load_json(path)


def string_to_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        pass


def date_to_string(date):
    return date.strftime("%Y-%m-%d")


def usage():
    print "usage %s twitter-query start-date [end-date]" % sys.argv[0]
    print "  start-date, end-date:  YYYY-mm-dd, e.g. \"2015-02-01\""


def usage_credentials():
    print "Your twitter API credentials must be available in a JSON file, \"credentials.json\""
    print "sample format:"
    print format_json({'consumer_key': "XXX",
                       'consumer_secret': "XXX",
                       'access_token': "XXX",
                       'access_token_secret': "XXX"})


def format_json(o):
    return json.dumps(o, indent=4, separators=(',', ': '))


def main():
    argc = len(sys.argv)
    if argc < 3 or argc > 4:
        usage()
        exit(-1)
        
    # not much error checking we can do here...
    q = sys.argv[1]

    start_date = string_to_date(sys.argv[2])
    if not start_date:
        usage()
        exit(-1)
        
    if argc == 4:
        end_date = string_to_date(sys.argv[3])
        if not end_date:
            usage()
            exit(-1)
    else:
        end_date = start_date
    
    credentials = load_credentials()
    if not credentials:
        usage_credentials()
        exit(-1)
        
    auth = tweepy_auth(credentials)
    api = tweepy_api(auth)
    
    one_day = datetime.timedelta(days=1)
    try:
        for since_date in date_partition(start_date, end_date):
            since = date_to_string(since_date)
            until = date_to_string(since_date + one_day)
            basename = "tweet_%s_%s" % (string.replace(q, " ", "+"), since)
            serializer = TweetSerializer(basename)
            try:
                print "running query q=\"%s\", since=%s, until=%s" % (q, since, until)
                count = 0
                for tweet in tweepy_query(api, q, since, until):
                    serializer.write(tweet)
                    count += 1
                print "  %s results" % count
            finally:
                # allows for cleanup on interrupt
                if serializer:
                    serializer.close()
    except KeyboardInterrupt:
        print "Interrupt caught, exiting..."


if __name__ == "__main__":
    main()
