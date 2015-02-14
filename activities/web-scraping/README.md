# Scraping the Web #

Getting information off the Web is often called "scraping".  Resources are downloaded via various means and then information is extracted from the 
resource by parsing the data received.  The most common data format is HTML but there are plenty of over kinds of data on the Web.

We interact with the Web by HTTP requests and responses.  A request sends a method (a verb like "GET") to a server and a resource path.  The server then responds
with a status code, various metadata, and possibly an entity body.  That entity body contains the data for the resource (e.g., the HTML).

We can easily interact with a resource via the [urllib2 python module](https://docs.python.org/2/howto/urllib2.html).

    import urllib2
    response = urllib2.urlopen("http://www.ischool.berkeley.edu/")
    html = response.read()
    print html

The response object is a file-like object.  You can get access to the message returned via the info() method that returns an [HTTPMessage instance from httplib](https://docs.python.org/2/library/httplib.html).


## Parsing HTML ##

We'll use the [beautifulsoup library](http://www.crummy.com/software/BeautifulSoup/) to parse HTML responses.

### Installing ###

You can install the library via pip:

    pip install beautifulsoup4
    
### Basic Usage ###

You can just parse the resource you retrieve:

    resource = urllib2.urlopen(sys.argv[1])
    html = bs4.BeautifulSoup(resource.read().decode('utf-8'))
    
The `html` object is an interface to the post-parsed tree produced from the HTML syntax.

### Activity ###

   1. Pick a Web page of your choice.
   2. Parse the Web page using BeautifulSoup
   3. Extract all the links (a `@href` attribute on `a` elements) from the document.
   
   