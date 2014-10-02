import sys
import os

for line in sys.stdin:
    try:
        print os.path.abspath(line),
    except:
        print