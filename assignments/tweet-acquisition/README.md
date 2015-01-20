# Acquiring and Storing Social Media Data #

## A Hypothetical Scenario ##

Minecraft is a popular game throughout the world that was 
[acquired last year (2014) by Microsoft](https://mojang.com/2014/09/yes-were-being-bought-by-microsoft/).  We'd like to 
assess the current sentiment of the acquisition by examining social media data.  Twitter is an obvious and easy choice 
as a place to start.


## Acquisition Task ##

Acquire relevant data around the Microsoft / Mojang for a recent week.  To accomplish this, do the following:

 1. Write an acquisition program that can acquire tweets for a specific date on the using the Tweepy python package.  The program should pull tweets
    for the #microsoft and #mojang hash tags simultaneously.
    
 2. Run your data analysis over a week period of time.  You should chunk your data as appropriate and give yourself the ability to re-run the process reliable in case of failures.
 
 3. Organize the resulting raw data into a set of tweets and store these tweets into S3.
 
 4. Analyze the tweets by producing a histogram (a graph) of the words.

 
## What to Turn In ##
 
1. A link to your S3 bucket documented in your README.md file.  Make sure to make it publicly accessible.

2. Your twitter acquisition code.

3. The histogram.


  