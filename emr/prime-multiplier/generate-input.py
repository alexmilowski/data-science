import sys
import random

max = int(sys.argv[1])
count = int(sys.argv[2])

def positiveRandom(max):
   n = random.random()
   while n==0:
      n = random.random()
   r = int(n*max)
   return 1 if r==0 else r
   
for i in range(count):
   print positiveRandom(max)