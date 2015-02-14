import urllib2

response = urllib2.urlopen("http://www.ischool.berkeley.edu/")
headers = dict(response.info())

for name in headers:
   print name,": ",headers[name]
