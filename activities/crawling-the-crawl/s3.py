from __future__ import print_function
import sys
from signal import signal, SIGPIPE, SIG_DFL

#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal(SIGPIPE,SIG_DFL) 

for line in sys.stdin:
   print("s3://aws-publicdatasets/"+line[0:-1])