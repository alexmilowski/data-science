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

# 2.1 Setup a Database, Starting, and Stopping #

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

Note: For the various code in this section we'll use the following logging functionss:

    var logError = function(error) { console.log(JSON.stringify(error, null, 2)); }
    var dumpResult = function(results) { results.forEach(function(result) { console.log(JSON.stringify(result.content, null, 2)); }); };

Also, refer to the [Node.js Application Developer's Guide](http://docs.marklogic.com/guide/node-dev) and the [Node.js API](http://docs.marklogic.com/jsdoc/index.html) for 
more information about the facilities described here for MarkLogic.

## 3.1 Creating a Database ##

You'll see that there are many options and features for databases.  You can safely ignore many of these features at this point but you do have
to understand a bit about the MarkLogic architure.

Databases use a collection of forests to store their actual data.  Forests are essentially disk-based storage.  A forest is made up of a set of stands 
that are managed automatically by the database.  As information in your database changes, the stands are replicated by a merge process.  This allows the
database to be both fast and consistent whilst achieving the ability to support ACID transactions.

To create a database, you need to:

   * create a database
   * create and assign forests to the database for storage
   
The general rule of thumb is three forests per database.

Once you started the MarkLogic server you'll want to create a database for this activity:

  1. Visit http://localhost:8001 in your browser.
  2. Click on "Databases" in the tree navigation on the left.
  3. Click on the "Create" tab.
  4. Type in 'tweets' in the "database name" field.
  5. Scroll through the options and turn on "word searches" and "collection lexicon".
  6. Click on "OK" to create the database.
  
You now need to create forests for the database:

  1. If you do not have the database selected in the tree navigation on the left, select the "tweets" database we just created.
  2. Select "Forests" from the navigation.
  3. Click on "Create a Forest".
  4. Type in "tweets-1" in the "forest name" field and leave all the other fields alone.
  5. Click on the "More Forests" button below to show another creation form.
  6. Type in "tweets-2" in the "forest name" field and leave all the other fields alone.
  7. Click on the "More Forests" button again to show another creation form.
  8. Type in "tweets-3" in the "forest name" field and leave all the other fields alone.
  9. Click on the "OK" button to create the three forests.
  10. Select all the forests in the "Configure Forests in a Database" view.
  11. Click on "OK" to attach the three newly created forests to the database.
  
## 3.2 Configuring connections ##

MarkLogic does not have one single default protocol for communication.  Instead, it supports a variety of connection methods of REST (HTTP), WebDAV, XDBC, and ODBC.  
For this activity, you need to configure a REST connection to your database so that Node can communicate with the MarkLogic server.

You cannot configure a REST end point through the admin console.  To do so, you must sent a POST:

   curl -X POST --anyauth --user admin:admin -d @rest-api.json -H "Content-Type: application/json" http://127.0.0.1:8002/LATEST/rest-apis
   
with the configuration information in a JSON document [rest-api.json](rest-api.json):

    { "rest-api": {
         "name": "RESTstop",
         "database": "tweets",
         "port": "8888"
       }
    }
    
You can test that you've done so correctly by accessing a simple REST API URI:

    $ curl --anyauth -u admin:admin http://127.0.0.1:8888/v1/values
    <rapi:values-list xmlns:rapi="http://marklogic.com/rest-api"/>

## 3.3 Connecting to a database ##

You can connect to a database by using the connection point and credentials you created previously:

    var marklogic = require('marklogic');
    var db = marklogic.createDatabaseClient({ host: 'localhost', port: '8888', user: 'admin', password: 'admin', authType: "DIGEST"});
   
In reality, this just configures the client.  Each connection over the protocol you are using will send authentication 
information.  In the above case, a request will use a HTTP DIGEST challenge response.

## 3.4 Inserting Data ##

MarkLogic supports a variety of data formats other than just JSON.  In this activity, we'll focus on the ability to store JSON data.

Documents can be written directly to the database simplying calling `write()` on `db.documents`:

    var docs = [ { uri: "/test/A.json", content: { id: "A", animal: "monkey" } }, { uri: "/test/B.json", content: { id: "B", animal: "dog" } }, { uri: "/test/C.json", content: { id: "C", animal: "cat" } } ];
    db.documents.write(docs).result(
       function(response) { response.documents.forEach(function(document) { console.log("Stored "+document.uri); }); },
       logError
    );
    
The method takes a single document description or an array of descriptions.

The description must have a `uri` property but may contain other metadata.  The most common options are:

   * `uri` — the URI of the document being stored
   * `content` — the JSON content object
   * `contentType` — the media type of the document (typically application/json) 
   * `collections` — an array of collection URIs to which this document belongs

You can update the metadata for a document by just omitting the `content` property.  The content of the document will remain the
same but any other metadata provided will be replaced by the operation.

## 3.5 Deleting Data ##

You can delete a single document by URI:

    db.documents.remove('/test/D.json').result(
       function(response) {
          console.log(JSON.stringify(response));
       } 
    );
    
Or a whole collection by URI:

    db.documents.removeAll({ collection: "/tests"}).result(
       function(response) {
          console.log(JSON.stringify(response));
       } 
    );

## 3.6 Querying Data ##

Through the Node.js API, queries built from functional expressions that compile into XQuery 
underneath.  A call to `db.documents.query()` returns a set of documents (or portions of them) 
that match your query.  From the query object you can specify various slices (partitions, portions,
etc.) that let you subset the matching results.

Note: we'll be using this abbreviation for the marklogic.queryBuilder API:

    var qb = marklogic.queryBuilder;

In this section, well use the following helper function"

A simple query by example can be constructed as:

    db.documents.query(qb.where(qb.byExample( { id: 'A' }))).result(dumpResult);
   
This will return all the documents that have a 'test' property that has the value 'A'.

In query by example, you can use combinations of properties and structures as well:

    db.documents.query(qb.where(qb.byExample( { id: 'A', animal: 'monkey' }))).result(dumpResult);

Results can be paginated by selecting a particular slice.  For example, the first three:
 
    db.documents.query(qb.where(qb.byExample( { id: 'A' })).slice(1,3)).result(dumpResult);
   
You can also use the `slice()` method to extract portions of the results.  This is useful if the resulting document
is complex or large and you only need a small portion.

The `extract` method takes a path expression (see [Traversing JSON Documents Using XPath](https://docs.marklogic.com/guide/app-dev/json#id_10326) ):

    db.documents.query(qb.where(qb.byExample( { id: 'A' })).slice(qb.extract("/animal"))).result(dumpResult);
    
You can read more about how to manipulate the query results in [Refining Query Results](http://docs.marklogic.com/guide/node-dev/search#id_24160).


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
  
  
