import numpy as np
import sys
import json
from pylab import *
from wordcloud import WordCloud

wcfile = open('./wordcount_test/part-00000')
total = 0
tokens, counts = [], []
for line in wcfile:
    tmp = json.loads(line.strip('\n'))
    tokens.append(tmp.keys()[0]), counts.append(tmp.values()[0])
    
counts = np.array(counts)
ranks = np.arange(1, len(counts)+1)
weights = counts.astype(float)/np.nansum(counts.astype(float))
idx_sort = np.argsort(-counts)

sorted_tokens = [tokens[i] for i in idx_sort]
loglog(ranks, counts[idx_sort], marker=".")
title("Zipf Distribution From Tweets")
xlabel("Rank of Tokens")
ylabel("Absolute frequency of token")
grid(True)

for n in list(logspace(-0.5, log10(len(counts)-1), 20).astype(int)):
    dummy = text(ranks[n], counts[idx_sort[n]], " " + sorted_tokens[n], 
                 verticalalignment="bottom",
                 horizontalalignment="left")

imajong = np.where(np.array(sorted_tokens) == 'majong')[0]
dummy = text(ranks[imajong], counts[idx_sort[imajong]], " " + sorted_tokens[imajong],  
                 verticalalignment="top",
                 horizontalalignment="right")
show()

wcd = []
for w,c in zip(sorted_tokens, weights[idx_sort]):
    wcd.append([w,c])


wordcloud = WordCloud(font_path='/Users/charlesmaalouf/Library/Fonts/Verdana.ttf')
wordcloud.fit_words(wcd)
imshow(wordcloud)


