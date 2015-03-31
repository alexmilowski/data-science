# Crawling the Commong Crawl #

The common crawl is a data set hosted by AWS that represents a crawl of the Web.  The data set contains the raw web pages as well as 
metadata and text extracts that are smaller in size.

The dataset is stored in [WARC format](http://en.wikipedia.org/wiki/Web_ARChive) (ISO 28500:2009) and consists of a textual stream of
records.  Each record contains a header of name/value pairs followed by an entity body (and encoded payload).

The [Common Crawl stores its data](http://commoncrawl.org/the-data/get-started/) in these format on S3 as hosted by AWS in the bucket
and prefix of `s3://aws-publicdatasets/common-crawl/`. Crawl data from 2013 onward has the key structure of `crawl-data/CC-MAIN-YYYY-DD/
and so, for example, the latest is stored at `s3://aws-publicdatasets/common-crawl/crawl-data/CC-MAIN-2015-06/`.

## Activity — Exploring the Data Set ##

### How is it stored and partitioned? ###

Use the AWS CLI to explore the data set (`s3://aws-publicdatasets/common-crawl/crawl-data/CC-MAIN-2015-06/`) by using the `aws s3 ...` command and answer the following:

 1. What is stored at the root?
 2. What summary metadata can you retrieve? 
 3. What are the various data formats you can process?
 4. How is the data set partitioned?
 
 ### WARC, WET, WAT ###
 
 1. There are three data resources stored by the common crawl: raw pages, metadata, and textual extraction.  Are they all stored in the same format?
 
 2. What do you need to process them?
 
 3. Retrieve a sample being careful not to download the whole dataset (it is large).
 
 4. Examine a sample WAT file.
 

## Activity — Extracting Domain Coverage ##

First you need to create (or reuse) an S3 bucket for this activity. Throughout this activity, we will use the name `mybucket` for the bucket 
name and you should replace that with your bucket name.

Also, you'll need your AWS key name so that you have SSH access to the cluster.

### Start a Cluster ###

First, copy the bootstrapping script [cc-bootstrap.sh](cc-bootstrap.sh) to the root of your bucket (e.g. to s3://mybucket/cc-bootstrap.sh):

    aws s3 cp cc-bootstrap.sh s3://mybucket/cc-bootstrap.sh

This script installs python 2.7 and various packages use by the WARC python modules.

There is a script in the code called [start.sh](start.sh) that uses the AWS CLI to start a basic cluster for this activity.  It takes a key name (for ssh) and bucket name as arguments:

    ./start.sh mykey mybucket
    
It will start the cluster defined in [cluster.json](cluster.json).
