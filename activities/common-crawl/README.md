# Common Crawl Exemplar #

This activity will step you through the process of running various Map/Reduce (MR) processes 
on the [Common Crawl](http://commoncrawl.org/) data set hosted by [AWS](http://aws.amazon.com).

In this activity you will:

  1. Install various supporting tools for running MR processes via [mrjob](https://github.com/Yelp/mrjob) and [AWS EMR](http://aws.amazon.com/elasticmapreduce/).
  2. Process data locally using mrjob.
  3. Run the same process on AWS EMR.
  4. Ensure you have all correct development environment to do the above.
  
This activity is divided into two parts.  In the first part, you'll run the example code locally.  Afterwards, you can setup an AWS account and role so that you can run the same 
process on AWS in the cloud.

We will be running the "[Tag Counter](https://github.com/commoncrawl/cc-mrjob#running-the-code)" over portions of the Common Crawl data set.
  
# General Setup #

## Shell Access ##

Most of the following code uses shell commands.  You should become familiar with running commands from the shell and make sure you have an environment that
matches your deployment environment (likely Linux).  You can run a Linux OS locally via technology like [Virtual Box](https://www.virtualbox.org).

## Get the Code via Git ##

You need to install git from [github](http://github.com) and you're already on their site.  If you haven't already done so, sign up for an account and clone the 
code for the [Common Crawl - mrjob starter kit](https://github.com/commoncrawl/cc-mrjob):

    git clone https://github.com/commoncrawl/cc-mrjob.git

This will download the code into whatever directory you are in when you issue that command.  You should then have a directory called 'cc-mrjob'.  The setup from now on 
will assume you are in the same directory.

If you do not have this repository, clone this into a parallel directory:

    git clone https://github.com/alexmilowski/data-science.git
   
You should now have two parallel directories:

    .../cc-mrjob/
    .../data-science/
   
Copy these files from `data-science/activities/common-crawl` to the `cc-mrjob` directory :

    mrcc.py
    mrcc.py.tar.gz
    mrjob.conf
   
Note: The modified code just fixes issues with pulling the common crawl data from S3 and the `mrjob.conf` is a configuration of EMR bit more specific to this activity.


## Setup Python ##

You should install [Python 2.7.8](https://www.python.org/download/releases/2.7.8/) locally so you can run this example.  If you have previous versions 
of Python, you may run into compatibility reasons (e.g. don't use 2.6.x).  In addition, Python 3.0 has many changes that also may be problematic.

You may find a Python IDE useful but you should ensure you can run Python from the command line properly.  Also, installing multiple versions of Python is not recommended.

Once you've gotten your Python install sorted, load the packages for the activity via pip:

    pip install -r requirements.txt
   
Note: Depending on how you have install various bits, you may need a "sudo" in front of that.

# Run it Locally #

## Requirements ##

You'll need good bandwidth to download the various data.

## Get the Data ##

There is a script that uses `wget` to download various content from the hosted dataset on S3:

    ./get-data.sh
    
 If you are on a Mac or Windows, you'll likely need to install wget.  If you use Mac Ports, you can install wget via:
 
     sudo port install wget
     
 Otherwise, the datasets for this activity are located at:
 
     https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/warc/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.gz
     https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wat/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wat.gz
     https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wet/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wet.gz

The various subsequent scripts expect a subdirectory structure of:

    common-crawl/
       crawl-data/
          CC-MAIN-2014-35/
             segments/
                1408500800168.29/
                   warc/
                      CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.gz
                   wat/
                      CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wat.gz
                   wet/
                      CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wet.gz

## Run the Code ##

To run the code, do the following:

    python absolutize_path.py < input/test-1.warc | python tag_counter.py -r local --conf-path mrjob.conf --no-output --output-dir out

The first python script just turns a relative path into an absolute path.  The second python uses that path as input via stdin and then runs the Map/Reduce process locally via mrjob.

The output is in the file `out/part-00000`.

    
# Run it on AWS EMR #

If you have not signed up for AWS, you'll need to do that first by visiting http://aws.amazon.com/

## AWS Setup ##

If you do not have a user/group with access to EMR, you'll need to do the following procedure.

First, you need to setup a user to run EMR:

 1. Visit http://aws.amazon.com/ and sign up for an account.
 2. Select the "Identity and Access Management" (or IAM) from your console or visit https://console.aws.amazon.com/iam/home
 3. Select "Users" from the list on the left.
 3. Click on the "Create New Users"
 4. Enter a user name for yourself and create the user.
 5. The next screen will give you an option to download the credentials for this user.  Do so and store them in a safe place.  You will not be able to retrieve them again.

Second, you need to create a group with the right roles:

 1. Select "Groups" from the list on the left.
 2. Click on "Create New Group".
 3. Enter a name and click on "Next Step".
 4. Scroll down to "Amazon Elastic MapReduce Full Access" click on "Select".
 5. Once the policy document is displayed, click on "Next Step".
 6. Click on "Create Group" to create the group.
 
Third, you need to assign your user to the group:

 1. Select the check box next to your group.
 2. Click on the "Group Actions" drop-down menu and click on "Add Users to Group".
 3. Select your user by clicking on the check box.
 4. Click on "Add Users".

## Configure mrjob ##

You need to configure mrjob to access your AWS account:

   1. Edit the mrjob.conf
   2. Locate the `#aws_access_key_id:` and `#aws_secret_access_key:` lines.
   3. Remove the hash (#) and add your AWS key and secret after the colon (:).  You should have these from previously creating the user.
   
## Setup an Output Bucket on S3 ##

You need to create an output bucket on S3 for the results of your computation:

   1. Go to https://aws.amazon.com/ in your browser.
   2. Click on the 'S3' service link.
   3. Click on the 'Create Bucket' button.
   4. Enter a name and hit create.
   
Keep in mind that the bucket name is unique to all of Amazon.  If you use some common name, it is likely to clash with other 
users.  One suggestion is to use a common prefix (e.g. a domain name) for all your bucket names.

## Run the Code on EMR ##

In the previous step, you created an output bucket.  In the example below, replace `{your-bucket-name}` with the name of the bucket you created.

To run the tag count on EMR for one input, do the following:

    time python tag_counter.py -r emr --conf-path mrjob.conf --python-archive mrcc.py.tar.gz --no-output --output-dir s3://{your-bucket-name}/cc-test-1 --source s3 input/test-1.warc
