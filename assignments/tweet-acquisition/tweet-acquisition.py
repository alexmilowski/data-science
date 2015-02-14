# David Paculdo
# W205 - Assignment 2
# Twitter Acquisition

import sys
import tweepy
import datetime
import urllib
import signal
import json
import os
import ast


def valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        sys.exit()


argnum = len(sys.argv)
argcount=range(1,argnum)

search_term="minecraft";
join_term="+AND+"
start_date="";
end_date="";
language="";
max_size=1000000;
term_count=0;
path_start="./"

for i in argcount:
    if sys.argv[i]=="-or":
        join_term="+OR+"
    if sys.argv[i]=="-help" or sys.argv[i]=="-h":
        print("Script accepts the following options (in lowercase):")
        print("  The following require no additional input:")
        print("    -help        To print this help screen.")
        print("    -or          Uses the 'or' option for multiple search terms. 'and' is default.")
        print("    -en          Restricts language to english. Default is no restrictions.")
        print("  The following require a single argument directly after:")
        print("    -search      Multiple -search can be used.")
        print("    -hash        Hashtag search. Do not input '#'. Multiple hashtags can be used.")
        print("    -user        Restrict to particular user.")
        print("    -start       Start date for search. Format expected is: YYYY-MM-DD.")
        print("    -until       End date for search. Format expected is: YYYY-MM-DD.")
        print("    -max         Max size of file in megabytes. Default is 1MB.")
        print("    -path        Enter path of output file. Default is current directory.")
        sys.exit()


for i in argcount:
    if sys.argv[i]=="-path":
        path_start=sys.argv[i+1]
    if sys.argv[i]=="-en":
        language="en"
    if sys.argv[i]=="-start" and start_date=="":
        start_date=sys.argv[i+1]
        valid_date(start_date)
    if sys.argv[i]=="-until" and end_date=="":
        end_date=sys.argv[i+1]
        valid_date(end_date)
    if sys.argv[i]=="-search":
        if term_count==0:
            search_term=sys.argv[i+1]
        else:
            search_term=search_term+join_term+"%s" %sys.argv[i+1]
        term_count+=1
    if sys.argv[i]=="-hash":
        if term_count==0:
            search_term="#%s" %sys.argv[i+1]
        else:
            search_term=search_term+join_term+"#%s" %sys.argv[i+1]
        term_count+=1
    if sys.argv[i]=="-max":
        max_size=int(sys.argv[i+1])*1000000


filepart=search_term.replace(" ","_")
filepart=search_term.replace("+","_")
filepart=filepart.translate(None, "#@!,.;")
if (start_date != ""):
    filepart=filepart+"_%s" % (start_date)
if (end_date != ""):
    filepart=filepart+"_%s" % (end_date)
filepath="%s%s" % (path_start, filepart)

q = urllib.quote_plus(search_term)  # URL encoded query

print("query: %s" % q)
print("start date: %s" % start_date)
print("until date: %s" % end_date)
print("language: %s" % language)
print("max file size: %i" %max_size)

#
# Twitter access key and tokens
#
consumer_key = os.environ.get("twitter_consumer_key");
consumer_secret = os.environ.get("twitter_consumer_secret");

access_token = os.environ.get("twitter_access_token");
access_token_secret = os.environ.get("twitter_access_token_secret");

# Twitter authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Twitter API Access
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


filenum=0
filename="%s_%i.raw" %(filepath, filenum)
tweets_only="%s_tweets_%i.txt" %(filepath, filenum)

try:
    my_file = open(filename,"w")
    tweet_file=open(tweets_only,"w")

    for tweet in tweepy.Cursor(api.search,q=q, start=start_date, until=end_date).items():
        tweet_string=str(tweet._json)

        tweet_dict=ast.literal_eval(tweet_string.encode("utf-8"))
        my_file.write(tweet_string+"\n")
        tweet_part=tweet_dict["text"]
        tweet_part=tweet_part.replace("\n"," ")
        tweet_file.write(tweet_part.encode("utf-8")+"\n")

        file_size=os.path.getsize("%s" % filename)

        if (file_size > max_size):
            my_file.close()
            #tweet_file.close()
            filenum+=1
            filename = "%s_%i.raw" % (filepath, filenum)
            #tweets_only = "%s_tweets_%i.txt" % (filepath, filenum)
            my_file = open(filename,"w")
            #tweet_file = open(tweets_only,"w")

    my_file.close()
    tweet_file.close()

except KeyboardInterrupt:
    print("Interrupt called")
    my_file.close()
    tweet_file.close()
    sys.exit()

