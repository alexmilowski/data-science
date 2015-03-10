import sys
import random
import os

prefix = sys.argv[1]
files = int(sys.argv[2])
max = int(sys.argv[3])

for n in range(files):
   f = open(prefix+"-"+str(n+1)+".txt","w")
   for i in range(max):
      f.write(str(n+1)+" "+str(i+1)+"\n")
   f.close();

