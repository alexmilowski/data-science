import sys
import random

# The maximum magnitude of the numbers
max = int(sys.argv[1])
# The number to generate
count = int(sys.argv[2])

def positiveRandom(max):
   n = random.random()
   while n==0:
      n = random.random()
   r = int(n*max)
   return 1 if r==0 else r
   
# Generate a positive random number for the count up to the given maximum
for i in range(count):
   print positiveRandom(max)