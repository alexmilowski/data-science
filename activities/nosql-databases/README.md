# NoSQL Databases #

[NoSQL ("Not Only SQL") databases](http://en.wikipedia.org/wiki/NoSQL) are databases that provide a mechanism for storing data that isn't
limited a "relational model" (tabular).  They often provide key/value, graph, or document-based storage and sometimes all of these combined.

Many such systems are focus on horizontal scaling based on clustering, partitioning data, and federating queries.  They are often coupled
with "big data analytics" but are not limited to such applications.  Such database are often better at handling a wider variety of data
with loose relations, semi-structure data formats such as XML or JSON, semantic graphs, and other non-relational models.

In this activity, we'll be looking at two popular document storage NoSQL databases: [MongoDB](https://www.mongodb.org) and [MarkLogic](http://www.marklogic.com)

# Setup #

You need to download and install MongoDB and MarkLogic in your development environment.  You can run both of these databases locally without too
much worry for this activity.  We won't be using that much data where you'll need a lot of disk space or memory.  Do keep in mind you are running
a database in addition to your other tools and they all consume memory—especially a database.

## MongoDB ##

1. Visit the [downloads page](http://www.mongodb.org/downloads) for MongoDB 2.6.7.
2. Choose the download for your platform (~100+ MB)
3. Follow the [install instructions](http://docs.mongodb.org/master/release-notes/2.6/) for your platform.

You should familarize yourself with the basics of starting and stopping the MongoDB server.

## MarkLogic ##

1. Visit the [downloads page](http://developer.marklogic.com/products) for MarkLogic 8.0-1.1
2. Choose the download for your platform (~150 MB)
3. Register as a developer (or login).
4. Follow the [installation guide](http://docs.marklogic.com/guide/installation) for your platform.

You should familarize yourself with the basics of starting and stopping the MarkLogic server.

## Node ##

While there is a REST API and various programming languages (Python) can be used to interface these databases,
we'll be using Node.js for these activities.  

1. Visit the [downloads page](http://nodejs.org/download/) for Node 0.12.0
2. Choose the download for your platform (~15MB)
3. Following the install instructions from the website.

Then you should install the node modules for both databases:

    npm install mongodb
    npm install marklogic

Note: Some users may need to use `sudo` in front of the above commands depending on how they installed node.


