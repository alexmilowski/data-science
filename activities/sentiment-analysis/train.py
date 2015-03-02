import sys
import nltk
import sets
import pickle

# Local
import featureset

wordlistFilename = sys.argv[1]
rangeSpec = sys.argv[2].split(",")
wordStart = int(rangeSpec[0])
wordEnd = int(rangeSpec[1])
outputFilename = sys.argv[3]

featureWords = featureset.load(wordlistFilename,wordStart,wordEnd)
print featureWords

sys.stderr.write("Loading training data...");

texts = []

for line in sys.stdin:
   parts = line.decode('utf-8').split("\n")[0].split("\t")
   wordlist = list(featureset.wordlist(parts[1]))
   texts.append((wordlist,parts[0]))

extractFeatures = featureset.makeExtractor(featureWords)

sys.stderr.write(" applying features ...");
trainingSet = nltk.classify.apply_features(extractFeatures, texts)

sys.stderr.write(" training classifier ...");
classifier = nltk.NaiveBayesClassifier.train(trainingSet)
sys.stderr.write(" done\n");

f = open(outputFilename, 'wb')
pickle.dump(classifier, f)
f.close()
