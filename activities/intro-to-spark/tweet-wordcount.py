import sys
import json
from pyspark import SparkContext

sc = SparkContext(appName="TweetWordCount")

# Load the JSON data from the file (or wildcard) on the command line
lines = sc.textFile(sys.argv[1], 1)

# count the words: load each line into a JSON object, split each text property, output a key/value pair (count of 1), reduce by summation
counts = lines.map(lambda line: json.loads(line)) \
              .flatMap(lambda tweet: tweet["text"].split()) \
              .map(lambda word: (word, 1)) \
              .reduceByKey(lambda a,b : a + b)

# output the results (unsorted)
output = counts.collect()
for (word, count) in output:
   print "{0}: {1}".format(word.encode("utf-8"), count)
