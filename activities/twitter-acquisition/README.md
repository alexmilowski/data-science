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
    
