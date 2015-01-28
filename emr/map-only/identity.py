#!/usr/bin/python
import sys

while True:
   data = sys.stdin.read(8192)
   if not data: break
   sys.stdout.write(data)