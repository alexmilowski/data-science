# NoSQL Databases #

[NoSQL ("Not Only SQL") databases](http://en.wikipedia.org/wiki/NoSQL) are databases that provide a mechanism for storing data that isn't
limited a "relational model" (tabular).  They often provide key/value, graph, or document-based storage and sometimes all of these combined.

Many such systems are focus on horizontal scaling based on clustering, partitioning data, and federating queries.  They are often coupled
with "big data analytics" but are not limited to such applications.  Such database are often better at handling a wider variety of data
with loose relations, semi-structure data formats such as XML or JSON, semantic graphs, and other non-relational models.

In this activity, we'll be looking at two popular document storage NoSQL databases: [MongoDB](https://www.mongodb.org) and [MarkLogic](http://www.marklogic.com)

# 1. Setup #

You need to download and install MongoDB and MarkLogic in your development environment.  You can run both of these databases locally without too
much worry for this activity.  We won't be using that much data where you'll need a lot of disk space or memory.  Do keep in mind you are running
a database in addition to your other tools and they all consume memory—especially a database.

## 1.1 MongoDB ##

1. Visit the [downloads page](http://www.mongodb.org/downloads) for MongoDB 2.6.7.
2. Choose the download for your platform (~100+ MB)
3. Follow the [install instructions](http://docs.mongodb.org/master/release-notes/2.6/) for your platform.

You should familiarize yourself with the basics of starting and stopping the MongoDB server.

## 1.2 MarkLogic ##

1. Visit the [downloads page](http://developer.marklogic.com/products) for MarkLogic 8.0-1.1
2. Choose the download for your platform (~150 MB)
3. Register as a developer (or login).
4. Follow the [installation guide](http://docs.marklogic.com/guide/installation) for your platform.

You should familiarize yourself with the basics of starting and stopping the MarkLogic server.

## 1.3 Node ##

While there is a REST API and various programming languages (Python) can be used to interface these databases,
we'll be using Node.js for these activities.  

1. Visit the [downloads page](http://nodejs.org/download/) for Node 0.12.0
2. Choose the download for your platform (~15MB)
3. Following the install instructions from the website.

Then you should install the node modules for both databases:

    npm install mongodb
    npm install marklogic

Note: Some users may need to use `sudo` in front of the above commands depending on how they installed node.

If you are not familiar with JavaScript, work through as much as you can via the [node.js JavaScript tutorial](https://github.com/sethvincent/javascripting).  JavaScript
is a fairly easy language to learn if you already know Python.

## 1.4 Summary ##

You should have:

  1. Setup MongoDB and understand how to stop and start it.
  2. Setup MarkLogic and understand how to stop and start it.
  3. Setup Node.js
  3. Have familiarized yourself with JavaScript and Node. 

# 2. MongoDB #

MongoDB is a JSON database that stores JSON "documents" in collections.  The main data unit is a JSON object (i.e. a "document") which are organized by named collections.

# 2.1 Setup a Database, Starting and Stopping #

If you haven't started MongoDB yet, there are two scripts to help you:

 * [setup.sh](mongo/setup.sh) — creates the basic directory structure
 * [forkdb.sh](mongo/forkdb.sh) - forks mongodb as a daemon and puts the process ID into a file (`mongo.pid`).

To get setup: 
 
 1. Create a directory for your test configuration.
 2. Copy the [mongo.conf](mongo/mongo.conf) file into that directory.
 3. Run `setup.sh` in that directory.
 4. Run `forkdb.sh` to start MongoDB.
 
 For example (assuming this directory):
 
     mkdir test
     cp mongo.conf test
     cd test
     ../setup.sh
     ../forkdb.sh
     
You should be able to confirm MongoDB is running by examining the `mongo.pid` file and looking for the process with the same identifier.

When you are done with MongoDB, you can simply send a SIGTERM signal to the process.  Never use SIGKILL as you'll likely end up with a corrupt database.

# 2.2 Getting Connected #

MongoDB runs on a particular host and port.  You can change this in the `mongo.conf` and is currently configured to bind to 
the local loopback address (127.0.0.1) on port 27017.

You can connect to Mongo via node by invoking node and using the following code:

    var MongoClient = require('mongodb').MongoClient,
        ObjectID = require('mongodb').ObjectID;
    
    // The database connection URI
    var url = 'mongodb://localhost:27017/test';
    
    // Connect to the database and provide a callback function
    MongoClient.connect(url, function(err, db) {
      console.log("Connected!");
      db.close();
    });

The above code scopes the database connection to the callback.  This lexical scoping is great for developing applications but for many of the following 
examples, we'll expose the database connection as a global variable with a small change:

    var MongoClient = require('mongodb').MongoClient;
    
    // The database connection URI
    var url = 'mongodb://localhost:27017/test';
    
    // Connect to the database and provide a callback function
    MongoClient.connect(url, function(err, db) {
      console.log("Connected!");
      global.db = db;
    });

If you then just type 'db' into the node console, you'll see a JSON representation of the connection object.

# 2.3 Inserting Data #

JSON documents (objects) are inserted into collections.  A collection is just a named set of documents.

You get a collection by:

    var collection = db.collection("conference");

Once you have a collection, you can insert documents:

    collection.insert({ test: "A" },function() { console.log("done!")});
    collection.insert({ test: "B" },function() { console.log("done!")});
    collection.insert({ test: "C" },function() { console.log("done!")});
    collection.insert({ test: "A" },function() { console.log("done!")});
    
Keep in mind that everything in Node is asynchronous with callbacks.  In theory, the data inserted above could be done in any order.

You can verify they have been inserted by the following:

   collection.find().toArray(function(err,docs) { console.log(docs); });
   
and the output might look like:

    >    collection.find().toArray(function(err,docs) { console.log(docs); });
    undefined
    > [ { _id: 54e79108867085b553abef7a, test: 'A' },
      { _id: 54e79108867085b553abef7b, test: 'B' },
      { _id: 54e79108867085b553abef7c, test: 'C' },
      { _id: 54e79109867085b553abef7d, test: 'A' } ]

Notice how each object gets a "_id" field.  This is the identifier assigned by the mongo DB and is of type ObjectID.  In queries and other requests, you need to construct this 
value via `ObjectID("54e79108867085b553abef7c")`.

## 2.3 Deleting Data ##

When delete data, you have several options:

   1. You can delete the database.
   2. You can delete the collection.
   3. You can delete a set of documents based on criteria.
   
For example, a single document can be deleted by its mongo identifier:

    collection.remove({ _id: ObjectID("54e79108867085b553abef7c") }, {w:1}, function(err, r) { console.log("Done!"); });
    
A collection can be deleted by dropping it from the database:

    collection.drop(function(err,reply) { ... });
    
A database can be similarly dropped:

    db.dropDatabase(function(err, result) { ... });
    
## 2.4 Querying Data ##

A simple query can be perform by match objects by example.  For example:

    collection.find({ test: 'A'}).each(function(err,item) { console.log(item); });
    
The `find()` method returns a [Cursor instance](http://mongodb.github.io/node-mongodb-native/2.0/api/Cursor.html) that you can
manipulate in various ways.  The argument is a "query".  In this case, it specifies a field value that must match exactly.

# 3. MarkLogic #

# 4. Activity #

We'll be doing the same activity with the same data for both databases.  There is a set of tweets collected for conference (XML Prague 2015) in the 
files `prague-2015-02-14.json` and `prague-2015-02-15.json`.  For both databases, we'll be doing the following tasks:

 1. Create a collection for the tweet data.
 2. Load the JSON data into memory.
 3. Store each tweet as a separate object/document into the collection.
 4. Query the data in various ways.
 5. Delete a tweets for a particular user and verify they do not exist.
 6. Drop the collection from the database.

We want to produce the following results by query and/or processing the data that has been stored:

 1. Retrieve all the tweets for a particular user.
 2. What is the user with the most tweets?
 3. What is the most used hash tag?
 4. How many tweets were produced for each 1/2 hour period (i.e. what period of time during the conference produced tweets)?

Note that, part of deleting tweets for a particular user requires that you can query and identify them as such.

You can easily load the JSON data from disk via:

    var json = JSON.parse(fs.readFileSync('prague-2015-02-14.json','utf-8'));
    
One you've complete the activity for both databases, attempt to answer the following questions.

Discussion questions:

  1. Even though the amount of data is small, what kinds of indices would be helpful to define?
  2. How does the query language affect the amount programming necessary in Node?
  3. At what point did your code revert to linear search or other such non-scalable algorithms?
  
  
