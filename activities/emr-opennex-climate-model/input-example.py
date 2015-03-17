from mrjob.job import MRJob
import sys
import os
import json
import math

class InputExample(MRJob):

   def mapper(self, _, line):
      obj = json.loads(line)
      yield "average",sum(obj["data"])/len(obj["data"])

   def reducer(self, key, values):
      data = list(values)
      yield key, sum(data) / len(data)


if __name__ == '__main__':
    InputExample.run()
