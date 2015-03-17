from mrjob.job import MRJob
import sys
import os
import json
import math
import datetime

import seqs
import date_partitions as partitions

class ListSequences(MRJob):

   def configure_options(self):
      super(ListSequences, self).configure_options()
      self.add_passthrough_option('--data-dir',help="The directory where the data is stored.")
      
   def year_seq(self,_,line):
      if line[0] == '#':
         return

      args = line.rstrip().split(",");
      
      quad = [ float(args[0]), float(args[1]),
               float(args[2]), float(args[3]) ]
      size = int(args[4])
      startYear = int(args[5])
      startMonth = int(args[6])
      endYear = int(args[7])
      endMonth = int(args[8])

      for month in partitions.month_partition(datetime.datetime(startYear,startMonth,1),datetime.datetime(endYear,endMonth,1)):
         for seq in seqs.sequencesFromQuadrangle(size / 120.0,quad):
            yield "{}-{:02d}".format(month.year,month.month),(size,seq)
            
   def average_quadrangle(self, yearMonth, quadSpec):
      size,seq = quadSpec
      fileName = self.options.data_dir+(os.sep if self.options.data_dir[-1]!=os.sep else "")+yearMonth+"-"+str(size)+"-"+str(seq)+".json"
      if os.path.exists(fileName):
         f = open(fileName,"r")
         obj = json.load(f)
         f.close()
         yield yearMonth,(1,len(obj["data"]))

   def steps(self):
        return [
            self.mr(mapper=self.year_seq,
                    reducer=None),
            self.mr(mapper=self.average_quadrangle,
                    reducer=None)
        ]      


if __name__ == '__main__':
   ListSequences.run()

