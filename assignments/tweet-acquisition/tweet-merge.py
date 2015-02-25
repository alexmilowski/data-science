#! /usr/bin/env python

__author__ = 'tkunicki'

import codecs
import glob
import json
import sys


def usage():
    print "usage: %s basename" % sys.argv[0]
    print "  basename: base file name to merge."

def main():
    argc = len(sys.argv)
    if argc != 2:
        usage()

    basename = sys.argv[1]
    
    tweet_in_filenames = glob.glob(basename + "_*.[0-9].json")
    tweet_in_filenames.sort()

    tweet_out_filename = basename + '.txt'
    with codecs.open(tweet_out_filename, 'w', encoding='utf8') as tweet_out_file:
        for tweet_in_filename in tweet_in_filenames:
            with codecs.open(tweet_in_filename, 'r', encoding='utf8') as tweet_in_file:
                tweets = json.loads(tweet_in_file.read().decode())
                for tweet in tweets:
                    tweet_out_file.write(tweet["text"] + "\n")
    print "wrote:", tweet_out_filename


if __name__ == "__main__":
    main()