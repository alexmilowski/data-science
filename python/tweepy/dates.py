import sys
import datetime

start = datetime.datetime.strptime(sys.argv[1],"%Y-%m-%d") # start date
end = datetime.datetime.strptime(sys.argv[2],"%Y-%m-%d")   # end date

def date_range(start,end):
   current = start
   while (end - current).days >= 0:
      yield current
      current = current + datetime.timedelta(days=1)
    
for d in date_range(start,end):
   print d