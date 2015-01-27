import urllib2

response = urllib2.urlopen("http://www.ischool.berkeley.edu/")
html = response.read()
print html