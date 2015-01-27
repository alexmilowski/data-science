import sys
import bs4
import urllib2

resource = urllib2.urlopen(sys.argv[1])
html = bs4.BeautifulSoup(resource.read().decode('utf-8'))
print "".join(html.title.strings)