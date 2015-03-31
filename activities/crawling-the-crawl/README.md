# Crawling the Common Crawl #

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

### 1. Start a Cluster ###

First, copy the bootstrapping script [cc-bootstrap.sh](cc-bootstrap.sh) to the root of your bucket (e.g. to s3://mybucket/cc-bootstrap.sh):

    aws s3 cp cc-bootstrap.sh s3://mybucket/cc-bootstrap.sh

This script installs python 2.7 and various packages use by the WARC python modules.

There is a script in the code called [start.sh](start.sh) that uses the AWS CLI to start a basic cluster for this activity.  It takes a key name (for ssh) and bucket name as arguments:

    ./start.sh mykey mybucket
    
It will start the cluster defined in [cluster.json](cluster.json).

*You'll need this cluster at the end.  Don't start the cluster until you need it a save yourself a bit a money.*

### 2. Get the manifest ###

At the root of the crawl there should be several compressed  manifest files that have paths to the data.  Retrieve these files from S3 and examine the WAT file.

The manifest contains a set of paths into the S3 bucket.  You can convert these to S3 URIs by:

    gzip -dc wat.paths.gz | python s3.py
    
### 3. Retrieve sample data ###

We will be working with the WAT metadata from here forward.  You may want to retrieve some sample data to work locally and then test your code on a cluster afterwards.

You can get the very first partition by:

    gzip -dc wat.paths.gz | python s3.py | head -n 1
    
You can use the AWS CLI to download this locally from S3.  Be warned that the data file is about 400MB in size.

Alternatively, you can use the `extract-CC-MAIN-20150124161055-00000-ip-10-180-212-252.ec2.internal.warc.wat.gz` file that is an extract of the first 907 records of the first partition.

### 4. View the data ###

Just take a peek:

    gzip -dc extract-CC-MAIN-20150124161055-00000-ip-10-180-212-252.ec2.internal.warc.wat.gz | more
    
What's in there?  Looks like JSON data ...

### 5. Run the example MRJob Locally ###

There is sample code in [mrcc.py](mrcc.py) and [ccex.py](ccex.py).

Run the example on the extract:

    echo `pwd`/extract-CC-MAIN-20150124161055-00000-ip-10-180-212-252.ec2.internal.warc.wat.gz | python ccex.py
    
What does that command do?

What did the program do?  Do you know how this works?

Notice something funny about the output?  Explain your observation based on the input data.


### 6. Modify the example ###

One basic issue with using the common crawl is to determine whether your target sites are in there.  Thus, one simple task is to count the domains crawled within
a particular data set.

Can you modify [ccex.py](ccex.py) to count domains?

The WAT data in WARC format contains metadata extracted from the crawl for each page.  Process the data to extract and count the domain names.  Be careful to remove sub-domains 
so that variants like `www1.hp.com` and `www2.hp.com` reduce to `hp.com`.

### 7. Run it on a cluster ###

Once you have your script read, you can run it directly on the dataset hosted in AWS.  All you need to do is provide a list of the S3 URIs you want to process as the input.

One simple way to do that is from the path metadata.  For example, the first 10 listed is:

    gzip -dc wat.paths.gz | python s3.py | head -n 10
    
There is a script called [run.sh](run.sh) that will launch your job on your cluster and it takes the script, the bucket, and the cluster identifier as parameters:

    gzip -dc wat.paths.gz | python s3.py | head -n 10 | ./run-step.sh myscript.py mybucket j-xxxxxxxxxxxxx

where `j-xxxxxxxxxxxxx` is your cluster identifier.

### 8. Discussion ###

How long will it take to compute the domains for a partition?  For the whole crawl date?  For the whole data set?

Does it scale?

What do you need to do to make it scale?

