from mrjob.job import MRJob
import sys
import os
import json
import math

# A simple example of processing JSON input to compute an average (w/o counts)
class InputExample(MRJob):

   # Yields an average for an input line (same key)
   def mapper(self, _, line):
      obj = json.loads(line)
      yield "average",sum(obj["data"])/len(obj["data"])

   # Computes the average over all the values
   def reducer(self, key, values):
      data = list(values)
      yield key, sum(data) / len(data)


if __name__ == '__main__':
    InputExample.run()
