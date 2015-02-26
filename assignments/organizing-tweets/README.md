# Organizing Acquired Data #

In this assignment we will be organizing the information like that acquired in 
[Acquiring and Storing Social Media Data](../tweet-acquisition).  In fact, 
we will be organizing it in three different ways and contrasting how the various 
storage systems can be used to accomplish a particular task.

The subject of the is the tweet data that was acquired from a conference:

  * [prague-2015-02-14.json](prague-2015-02-14.json)
  * [prague-2015-02-15.json](prague-2015-02-15.json)
  
Note: The time of the conference is CET (+01:00) timezone.
  
We need to answer the following questions by "querying" the data:

 1. Who tweeted the most during the conference?
 2. What were the top 10 hash tags used?
 3. For a particular hour, how many tweets were produced?

We are going to answer these questions using three different database storage techonlogies:

  * Key/Value — [AWS S3](http://aws.amazon.com/s3/)
  * NoSQL Database — [Mongo](https://www.mongodb.org) or [MarkLogic](http://www.marklogic.com)
  * Relational Database — SQLite, MySQL, etc.
  
## Tasks ##

As you look at the following tasks, keep in mind that you don't need all the raw information from the tweet
data as provided from Twitter.  That is, you do not need to model or store all the raw information but just
that which is sufficient to answer the tree questions.

  1. Draw a UML ER diagram how you would model your information extracted from the raw tweet data.
  2. For each database category of Key/Value, NoSQL, and Relational, decribe a systems architecture that contains:
     1. Your implementation model of how data is actually organized (e.g. a schema, collection structure, etc.).
     2. The process necessary to store the information into your implementation model.
     3. Pseudo-code / procedures that describe how you would answer each of the questions.
  3. For just one of the database categories, implement your architecture.

## What to turn in ##

1. Your UML ER diagram.
2. A document for each of the database categories for task #2.
3. Your implementation code for task #3.
4. The answers for each of the three questions.  Please provide answers for the hours 9:00+01:00 through 16:00+01:00 on both days.