import sys
import json
from pyspark import SparkContext

sc = SparkContext(appName="TweetLoader")
tweetData = sc.textFile("2015-02*.txt")
counts = tweetData.map(lambda line: json.loads(line)) \
                  .map(lambda tweet: (tweet["user"]["screen_name"],1)) \
                  .reduceByKey(lambda a,b: a + b)

output = sorted(counts.collect(),lambda a,b: b[1] - a[1])
for (user,count) in output:
   print "{}: {}".format(user,count)
