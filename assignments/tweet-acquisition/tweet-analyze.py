#! /usr/bin/env python

__author__ = 'tkunicki'

import codecs
import math
import operator
import string
import sys
# sudo pip install git+git://github.com/amueller/word_cloud.git
#sudo pip install Image
from wordcloud import WordCloud


def usage():
    print "usage: %s filename" % sys.argv[0]
    print "  basename: base file name to merge."


def main():
    argc = len(sys.argv)
    if argc != 2:
        usage()

    tweet_in_filename = sys.argv[1]

    histogram = {}
    with codecs.open(tweet_in_filename, 'r', encoding='utf8') as tweet_in_file:
        for tweet in tweet_in_file:
            words = [word.lower().strip(string.punctuation) for word in tweet.split() if not
            (word.startswith('#') or word.startswith('@') or word.startswith('http'))]
            for word in words:
                if len(word) > 0:
                    histogram[word] = histogram.get(word, 0) + 1

    count_max = 0
    word_max = 0
    for word, count in histogram.items():
        if len(word) > word_max:
            word_max = len(word)
        if count > count_max:
            count_max = count

    histogram_sorted = sorted(histogram.items(), key=operator.itemgetter(1), reverse=True)
    count_range = 80 - math.ceil(math.log10(count_max)) - 1
    count_max_log = math.log(count_max)
    with codecs.open(tweet_in_filename.replace(".txt", ".hist.txt"), 'w', encoding='utf8') as hist_out_file:
        for word, count in histogram_sorted:
            hist_out_file.write("%s\n" % word)
            hist_out_file.write("%s %s\n" % ('#' * int(math.log(count) / count_max_log * count_range), count))
        hist_out_file.write("\n")
            
    wc = WordCloud(font_path='/Library/Fonts/Verdana.ttf', width=800, height=400)
    wc.fit_words(map(lambda (x, y): (x, float(y) / count_max), histogram_sorted))
    wc.to_file(tweet_in_filename.replace(".txt", ".png"))


if __name__ == "__main__":
    main()