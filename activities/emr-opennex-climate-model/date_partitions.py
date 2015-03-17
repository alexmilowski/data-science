import sys
import datetime

# A date partition library

xsdDatetimeFormat = "%Y-%m-%dT%H:%M:%S"
xsdDateFormat = "%Y-%m-%d"

# A generator for date/times based on durations
#
def datetime_partition(start,end,duration):
   current = start
   while start==current or (end-current).days > 0 or ((end-current).days==0 and (end-current).seconds>0):
      yield current
      current = current + duration
      
# A generator for months given a start and end month.
#
# Example: Generates the months from 2015-03 to 2016-03
#
# months = month_partition(datetime.datetime(2015,3,1),datetime.datetime(2016,3,1))
#  
def month_partition(start,end):
   current = datetime.datetime(start.year,start.month,1)
   while current.year<end.year or (end.year==current.year and current.month<=end.month):
      yield current
      year, month= divmod(current.month+1, 12)
      if month == 0: 
         month = 12
         year = year -1
      current = datetime.datetime(current.year + year, month, 1)

# A generator for enumerating the days between two dates
#
# Example: The days from 2015-02-01 to 2015-05-15
#
# days = date_partition(datetime.datetime(2015,2,1),datetime.datetime(2015,5,15))
#
def date_partition(start,end):
   return datetime_partition(start,end,datetime.timedelta(days=1))

if __name__ == "__main__":
   start = datetime.datetime.strptime(sys.argv[1],xsdDateFormat) # start date
   end = datetime.datetime.strptime(sys.argv[2],xsdDateFormat)   # end date
   
   for d in date_partition(start,end):
      print d