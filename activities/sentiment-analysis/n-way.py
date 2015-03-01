import nltk

A = [ 
("A white dog","A"),
("The dog is white","A"),
("I have a fluffy white dog","A"),
("My dog is white","A")
]

B = [
("My cat is black","B"),
("There is a black cat","B"),
("Beware of the black cat","B"),
("The black cat is a short story","B")
]

C = [
("The parrot is green","C"),
("A parrot has green, blue, and red feathers","C"),
("A Green parrot is hard to see in the trees","C"),
("My parrot is not green","C")
]

data = [
"My dog hudson is white and grey", #A
"Sasha is a long-haired black cat", #B
"Buddy was my green parrot" #C
]

# words we will exclude
stopWords = [
"and",
"the"
]

# process the tweets into a training set of words
input = []
for (sentence, sentiment) in A + B + C:
    words = [e.lower() for e in nltk.word_tokenize(sentence) if len(e) >= 3 and not e.lower() in stopWords]
    input.append((words, sentiment))
    
print input
    

# Get an ordered list of most frequently used words    
def getAllWords(input):
    all = []
    for (words, sentiment) in input:
      all.extend(words)
    return all
    
print
    
wordlist = nltk.FreqDist(getAllWords(input))
print wordlist.pprint(100)
wordFeatures = wordlist.keys()
    
def extractFeatures(document):
    words = set(document)
    features = {}
    for word in wordFeatures:
        features['contains(%s)' % word] = (word in words)
    return features
    
trainingSet = nltk.classify.apply_features(extractFeatures, input)

classifier = nltk.NaiveBayesClassifier.train(trainingSet)

print
for sentence in data:
   print classifier.classify(extractFeatures(sentence.split())),": ",sentence






