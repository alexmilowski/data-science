import sys
import json
from pyspark import SparkContext

sc = SparkContext(appName="TweetLoader")
tweetData = sc.textFile("2015-02*.txt")
tweets = tweetData.map(lambda line: json.loads(line)) 

output = tweets.collect()
for (tweet) in output:
   print tweet
