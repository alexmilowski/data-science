import sys
import json
from pyspark import SparkContext

sc = SparkContext(appName="TweetLoader")
tweetData = sc.textFile("2015-02*.txt")
users = tweetData.map(lambda line: json.loads(line)) \
                 .flatMap(lambda tweet: [tweet["user"]["screen_name"]] + map(lambda u : u["screen_name"],tweet["entities"]["user_mentions"])).distinct()

output = users.collect()
for user in output:
   print user
