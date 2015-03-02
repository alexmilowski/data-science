import sys
import pickle
import sets
import nltk

# Local
import featureset

classifierFilename = sys.argv[1]
wordlistFilename = sys.argv[2]
rangeSpec = sys.argv[3].split(",")
wordStart = int(rangeSpec[0])
wordEnd = int(rangeSpec[1])

f = open(classifierFilename,"rb")
classifier = pickle.load(f)
f.close()

featureWords = featureset.load(wordlistFilename,wordStart,wordEnd)

reviews = []

extractFeatures = featureset.makeExtractor(featureWords)

count = 0
missed = 0
variance = 0;
for line in sys.stdin:
   parts = line.decode('utf-8').split("\n")[0].split("\t")
   wordlist = list(featureset.wordlist(parts[1]))
   c = classifier.classify(extractFeatures(wordlist))
   a = parts[0]
   count += 1
   if c != a:
      missed += 1
   print str(count)+"\t"+a+"\t"+c+"\t"+(",".join(reduce(lambda l,w: l+[w] if w in featureWords else l,wordlist,[])))

if count>0:
   print "{0} % correct, {1}/{2}  ".format(100* ((count-missed)*1.0 / count), (count-missed),count)