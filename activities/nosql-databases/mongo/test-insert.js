var MongoClient = require('mongodb').MongoClient,
    ObjectID = require('mongodb').ObjectID;

// The database connection URI
var url = 'mongodb://localhost:27017/test';

// Connect to the database and provide a callback function
MongoClient.connect(url, function(err, db) {
  console.log("Connected!");
  var collection = db.collection("conference");
  collection.insert(
     [{ test: "A" },{ test: "B" },{ test: "C" },{ test: "A" }],
     function() { 
        console.log("done!")
        db.close();
     }
   );
});
