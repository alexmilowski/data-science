import sys
import nltk
import sets
import operator

import featureset

words = {}

for line in sys.stdin:
   for word in featureset.wordlist(line.decode('utf-8')):
      words[word] = words[word] + 1 if word in words else 1

wordsSorted = sorted(words.items(), key=operator.itemgetter(1),reverse=True)

for w in wordsSorted:
   sys.stdout.write("{0}\t{1}\n".format(w[0].encode('utf-8'),w[1]))
   
