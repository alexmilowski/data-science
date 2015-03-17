#!/usr/bin/python
import sys

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
            
         
primes = [2, 3, 5]
counts = [0 for i in range(len(primes))]
for line in sys.stdin:
   i = int(line)
   if (i==0):
      continue
   p = 0;
   while i!=1:
      #print i,p,i % primes[p],counts
      while i!=1 and i % primes[p] == 0:
         i = i / primes[p]
         counts[p] += 1
      p += 1
      if i!=1 and p==len(primes):
         appendPrime(primes)
         counts.append(0)
         
for i in range(len(primes)):
   if counts[i]>0:
      print "LongValueSum:",primes[i],"\t",counts[i]