#!/usr/bin/python
import sys

# Appends a single next prime
def appendPrime(primes):
   p = primes[-1]
   prime = False
   while not prime:
      p += 1
      divisor = False
      for i in range(0,len(primes)):
         if p  % primes[i] == 0:
            divisor = True
            break
      if not divisor:
         prime = True
   primes.append(p)
   return primes
            
      
# an initial set of primes   
primes = [2, 3, 5]
# an initial array of zeros of the same length
counts = [0 for i in range(len(primes))]

# for each line of input, factor the input
for line in sys.stdin:

   # Parse the integer and skip zeros
   i = int(line)
   if (i==0):
      continue
      
   # Factor until we reach 1
   p = 0;
   while i!=1:
      #print i,p,i % primes[p],counts
      
      # compute exponent for current prime
      while i!=1 and i % primes[p] == 0:
         i = i / primes[p]
         counts[p] += 1
         
      # increment prime
      p += 1
      
      # if we aren't at zero but have run out of primes, find the next prime to factor
      if i!=1 and p==len(primes):
         appendPrime(primes)
         counts.append(0)

# Output the counts for each prime         
for i in range(len(primes)):
   if counts[i]>0:
      print "LongValueSum:",primes[i],"\t",counts[i]