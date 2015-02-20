#!/bin/bash
MONGO=$HOME/workspace/mongodb-osx-x86_64-2.6.5/

$MONGO/bin/mongod --config mongo.conf --pidfilepath `pwd`/mongo.pid
