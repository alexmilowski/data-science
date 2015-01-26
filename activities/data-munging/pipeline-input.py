import sys
import json

for line in sys.stdin:
   print line
   f = open(line.strip(),"r")
   # process data
   f.close()
