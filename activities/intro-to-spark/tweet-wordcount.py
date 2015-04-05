import sys
import json
from pyspark import SparkContext

sc = SparkContext(appName="TweetWordCount")
lines = sc.textFile(sys.argv[1], 1)
counts = lines.map(lambda line: json.loads(line)) \
              .flatMap(lambda tweet: tweet["text"].split()) \
              .map(lambda word: (word, 1)) \
              .reduceByKey(lambda a,b : a + b)

output = counts.collect()
for (word, count) in output:
   print "{}: {}".format(word.encode("utf-8"), count)