import sys
from pyspark import SparkContext

sc = SparkContext(appName="PythonWordCount")
lines = sc.textFile(sys.argv[1], 1)
counts = lines.flatMap(lambda x: x.split()) \
              .map(lambda word: (word, 1)) \
              .reduceByKey(lambda a,b : a + b)

output = counts.collect()
for (word, count) in output:
   print "{}: {}".format(word.encode('utf-8'), count)
