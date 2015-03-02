import sets
import nltk

stopWords = nltk.corpus.stopwords.words('english')

lemmatizer = nltk.stem.WordNetLemmatizer()

def wordlist(line):
   for word in [e.lower() for e in nltk.word_tokenize(line) if len(e) >= 3 and not e.lower() in stopWords]:
      if word == "n't":
         word = "not"
      if word == "'re":
         word = "are"
      if word == "'ve":
         word = "have"
      if word == "'ll":
         word = "will"
      word = lemmatizer.lemmatize(word)
      yield word


def load(filename,start,end):
   featureWords = sets.Set()
   input = open(filename,"r")
   count = 0
   for line in input:
      count += 1
      if count < start:
         continue
      if end>start and count > end:
         break
      parts = line.decode('utf-8').split("\n")[0].split("\t")
      featureWords.add(parts[0])
   input.close()
   return featureWords
   
def makeExtractor(featureWords):
   def extractFeatures(document):
       words = set(document)
       features = {}
       for word in featureWords:
           features['contains(%s)' % word] = (word in words)
       return features
   return extractFeatures
