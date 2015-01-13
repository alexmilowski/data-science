# Acquiring Data from Twitter #

This activity will step you through the process of acquiring data from Twitter and applying different acquisition strategies.

## Setup ##

### Install Tweepy ###

The code provided and activities will use the [tweepy](https://github.com/tweepy/tweepy) module.  You should install this package:

    pip install tweepy

### Create an Application ###

Twitter data can be accessed over the Web by creating an application on their site and then using the access keys
they provide for the application in your program.  

Note: You will need to have a Twitter account to create an application.

To create an application, follow this procedure:

 1. Login to Twitter (https://www.twitter.com/).
 2. Visit https://apps.twitter.com and click on "Create New App".
 3. Fill in the application name, description, and Website.  The name will be listed in your application list when you return this Website.
 4. Agree to the terms and agreements and click on "Create your Twitter Application"
 
Once you have successfully created an application, it should take you to the newly created application.  Here you must create access keys for 
subsequent operations by your application.  To do so, use the following procedure:

 1. Click on the "Keys and Access Tokens" tab.
 2. Click on "Create my Access Token" near the bottom of the page.
 
The response should be relatively immediate.

Now you have for things:

 1. A consumer key that identifies your application.
 2. A consumer secret that acts as a "password" for your application.
 3. An access token that identifies your authorized access.
 4. An access token secret that acts as a "password" for that authorized access.
 
At any point, you can revoke the access key or regenerated any of these values.
 
To completely disable the application, you must delete the application.  This does is remove the consumer key, secret, and access tokens from
Twitter's system and any program using them will immediately stop working.
 
### Test your Application ###
 
Use the `hello-twitter.py` program to test your application.  Change the code and insert your consumer key, consumer secret, access token, and 
access token secret.  You should then be able to just run the program and get a few tweets:

    python hello-twitter.py 
    
## Data Collection Activities ##

While real-time data collection is interesting, if you are research data provided by tweets, search is the simple way to 
collect information - even from the recent past.  Instead of collecting information and sorting it ourselves, we'll use 
the twitter search API to partition information by date/time and other facets to partition the collected data.

Also, the [Twitter API is rate limited](https://dev.twitter.com/rest/public/rate-limiting) and so you can't make more than 
180 requests per 15 minutes.  Fortunately, the tweepy library that we'll be using handles pausing automatically.  With the 
partitioning and the automatic handling of rate limiting against the [Twitter REST API](https://dev.twitter.com/rest/public), 
we'll be able to just write our code normally and the calls will pause until requests can be made again.

### The Tweepy Library ###

The Tweepy library handles talking directly to the various REST Web services provided by Twitter.  Many of the calls
have practical limits to the amount of data that is returned.  If you are trying to gather large amounts of data from
Twitter, you'll need to navigate the paged results.

Tweepy provides a "cursor" functionality that handles the navigation of paged results for you.  You simply
wrap your call in a Cursor object:

    for tweet in tweepy.Cursor(api.search,q=q).items(200)
       print tweet.text

In the above example, the 200 tweets are returned from the generator regardless of how many are returned from
each call to a Twitter REST API.

An example of this is shown in `search.py` where the first 200 tweets are collected for a search term.  You'll need to modify
the code to add your consumer key/secret and access token/secret.