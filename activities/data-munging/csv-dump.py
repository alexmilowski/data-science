import sys
import csv

for line in sys.stdin:
   f = open(line.strip(),"r")
   # process data
   reader = csv.reader(f,delimiter=',',quotechar='"')
   for row in reader:
      print ','.join(row)
      
   f.close()
