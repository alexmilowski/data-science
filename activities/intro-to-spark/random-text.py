import random
import sys

words = sys.stdin.read().splitlines()

for i in range(int(sys.argv[1])):
   for j in range(int(sys.argv[2])):
      sys.stdout.write(random.choice(words))
      sys.stdout.write(" ")
   sys.stdout.write("\n")


