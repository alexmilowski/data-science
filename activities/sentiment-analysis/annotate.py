import sys

for line in sys.stdin:
   sys.stdout.write(sys.argv[1])
   sys.stdout.write('\t')
   sys.stdout.write(line)