#! /usr/bin/env python

import boto
from boto.s3.key import Key
import json
import string
import nltk
from nltk.corpus import stopwords
import pandas as pd

import seaborn as sns
sns.set(context = 'notebook', style = 'darkgrid', palette='hls', rc={"figure.figsize": (17, 8)})

def freqdist(tweets):
    words = []
    s_words = stopwords.words('english')
    s_words.extend([u'', u'rt'])
    # we also want to strip out the RT marker, and anything that is blank after stripping punctuation
    for tweet in tweets:
        text = tweet['text']
        words.extend([
            w.lower().strip(string.punctuation)
            for w in nltk.tokenize.word_tokenize(text)
            if not (w.startswith('#') or w.startswith('@') or w.startswith('http')
                    or (w.lower().strip(string.punctuation) in s_words))
        ])
    fd = nltk.FreqDist(words)
    dist = sorted(fd.items(), key=lambda x: x[1], reverse=True)
    dist = pd.DataFrame(dist)
    dist = pd.Series(dist[1].values, index=dist[0])
    return dist


if __name__ == "__main__":
    conn = boto.connect_s3()  # connect to S3
    bucket = conn.get_bucket('janakmayer.berkeley.storingretrieving')
    k = Key(bucket)
    tw = []  # we are going to put all the tweets from all 7 days in here
    for i in range(5, 6):
        # Get tweets from 7 different json files for the 7 days of data
        k.key = 'twitter-assignment/tweets-%s.json' % i
        tw.extend(json.loads(k.get_contents_as_string()))
    d = freqdist(tweets=tw)
    print d[:50]  # Print the top 50 words
    plot = d[:50].plot(kind='barh')  # Plot a bar chart of the top 50 words
    fig = plot.get_figure()
    fig.savefig('tweet_graph.pdf')