import sys
import datetime

def datetime_partition(start,end,duration):
   current = start
   while start==current or (end-current).days > 0 or ((end-current).days==0 and (end-current).seconds>0):
      yield current
      current = current + duration
      
def date_partition(start,end):
   return datetime_partition(start,end,datetime.timedelta(days=1))

if __name__ == "__main__":
   start = datetime.datetime.strptime(sys.argv[1],"%Y-%m-%d") # start date
   end = datetime.datetime.strptime(sys.argv[2],"%Y-%m-%d")   # end date
   
   for d in date_partition(start,end):
      print d