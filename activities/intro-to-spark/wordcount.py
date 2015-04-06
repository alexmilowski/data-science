import sys
from pyspark import SparkContext

sc = SparkContext(appName="PythonWordCount")

# Load the data from the file (or wildcard) on the command line
lines = sc.textFile(sys.argv[1], 1)

# count the words: split each line, output a key/value pair (count of 1), reduce by summation
counts = lines.flatMap(lambda x: x.split()) \
              .map(lambda word: (word, 1)) \
              .reduceByKey(lambda a,b : a + b)
              
# output the results (unsorted)
output = counts.collect()
for (word, count) in output:
   print "{}: {}".format(word.encode('utf-8'), count)
