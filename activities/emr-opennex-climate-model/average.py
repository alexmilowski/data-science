from mrjob.job import MRJob
import sys
import os
import json
import math

# Computes the average correctly for a given input dataset
class Average(MRJob):

   # Loads the JSON object and yields yearMonth -> (length,average)
   def average_partition(self, _, line):
      obj = json.loads(line)
      #print obj["yearMonth"],(len(obj["data"]),sum(obj["data"])/len(obj["data"]))
      yield obj["yearMonth"],(len(obj["data"]),sum(obj["data"])/len(obj["data"]))

   # Combines sequence number averages for particular year+month
   def average_month(self, yearMonth, countAverage):
      sum = 0
      total = 0
      for count,value in countAverage:
         sum += count*value
         total += count
      #print yearMonth,(total,sum/total)
      yield "month",(total,sum/total)

   # Computes the average over the year/month data keeping track of counts
   def average(self,_,averageData):
      sum = 0
      total = 0
      for count,average in averageData:
         sum += count*average
         total += count
      #print "average",sum/total
      yield "average",sum/total
      
   # Define a 1-step job with a mapper, combiner, and reducer
   def steps(self):
        return [
            self.mr(mapper=self.average_partition,
                    combiner=self.average_month,
                    reducer=self.average)
        ]      


if __name__ == '__main__':
    Average.run()
