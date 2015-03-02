import nltk

# negative
negative = [ 
("We're all aware by now that Candy corn is evil","nasty"),
("Candy corn is so bad for you","nasty"),
("If you eat candy corn... I guess you would eat crayons, candles and ear wax too","nasty"),
("Candy corn is nasty","nasty"),
("Never not horrified by candy corn.","nasty")
]

# positive
positive = [
("I'm craving candy corn","best"),
("I still love candy corn","best"),
("Yes, I tweet candy corn and not broccoli. You know why? Because candy corn is more exciting.","best"),
("Autumn candy corn. So sweet; so good; so sticky. I taste no regrets.","best"),
("I love candy corn","best"),
("Candy corn is good","best")
]

# Test
tests = [
"Now's as good a time as any to remind you candy corn is the worst and if you like it you have a deep personal failing that needs examining.", #nasty
"Candy corn is my favorite candy on Halloween", #best
"Candy corn is sugar and wax - nasty", #nasty
"Can't get enough candy corn love", #best
"Candy corn is evil",  #nasty
"Candy corn is bad candy"  # nasty
]

# words we will exclude
stopWords = [
"candy",
"corn",
"and",
"not",
"the",
"...",
"'re"
]

# process the texts into a training set of words
texts = []
for (tweet, sentiment) in positive + negative:
    words = [e.lower() for e in nltk.word_tokenize(tweet) if len(e) >= 3 and not e.lower() in stopWords]
    texts.append((words, sentiment))
    
print texts
    

# Get an ordered list of most frequently used words    
def getAllWords(texts):
    all = []
    for (words, sentiment) in texts:
      all.extend(words)
    return all
    
print
    
wordlist = nltk.FreqDist(getAllWords(texts))
print wordlist.pprint(100)
wordFeatures = wordlist.keys()
    
def extractFeatures(document):
    words = set(document)
    features = {}
    for word in wordFeatures:
        features['contains(%s)' % word] = (word in words)
    return features
    
trainingSet = nltk.classify.apply_features(extractFeatures, texts)

classifier = nltk.NaiveBayesClassifier.train(trainingSet)

print
for tweet in tests:
   print classifier.classify(extractFeatures(tweet.split())),": ",tweet






