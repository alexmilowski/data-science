import json
import sys

data = json.load(sys.stdin)

for tweet in data:
   print json.dumps(tweet)