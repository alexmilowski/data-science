# Introduction to Spark #

## Setup ##

### Installing Spark ###

  1. Visit the Spark [Downloads](https://spark.apache.org/downloads.html) page.
  2. Select "1.3.0" from the first list box.
  3. Select "Pre-built for Hadoop 2.4 and later".
  4. Leave "Select Apache Mirror" alone.
  5. Click on the link in #4
  6. When the result page loads, click on the suggested mirror to download Spark.
  
Once you have downloaded Spark, just unpack the directory somewhere convenient.  We'll be using the executable directly from the distribution.

We'll use the environment variable `$SPARK_HOME` throughout this example.  You should define it to be where you unpacked the Spark distribution:

    export SPARK_HOME=~/workspace/spark-1.3.0-bin-hadoop2.4/
    
You should install psutil as well:

    pip install psutil

### Preparing Sample Data ###

We'll be using the same conference data from the [Organizing Acquired Data](../../assignments/organizing-tweets/) assignment.  We will prepare the data by writing each tweet onto a single line:

    python one-line-json.py < ../../assignments/organizing-tweets/prague-2015-02-14.json > 2015-02-14.txt
    python one-line-json.py < ../../assignments/organizing-tweets/prague-2015-02-15.json > 2015-02-15.txt
        
We'll also use some randomly generated files:

    curl "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain" > words
    mkdir random
    python random-text.py 1000000 10 < words > random/random-0.txt
    python random-text.py 1000000 10 < words > random/random-1.txt
    python random-text.py 1000000 10 < words > random/random-2.txt
    python random-text.py 1000000 10 < words > random/random-3.txt
    python random-text.py 1000000 10 < words > random/random-4.txt
    python random-text.py 1000000 10 < words > random/random-5.txt
    python random-text.py 1000000 10 < words > random/random-6.txt
    python random-text.py 1000000 10 < words > random/random-7.txt
    python random-text.py 1000000 10 < words > random/random-8.txt
    python random-text.py 1000000 10 < words > random/random-9.txt


## Activity - Run some example ##

### Hello World - Word Count ###

The classic "hello world" of map/reduce is a simple word count.  An example implementation is in [wordcount.py](wordcount.py) and can be run as follows:

    $SPARK_HOME/bin/spark-submit wordcount.py "random/random-*.txt"
    
This will run the word count over the randomly generated data (from the setup) of 100 million words.

The RDD contains a wild card and is effectively the same as:

    lines = sc.textFile("random/random-*.txt", 1)
    
and the wild card allows Spark to access all the generated data files.

The code is straight forward and starts with splitting the lines of text into words:

    lines.flatMap(lambda x: x.split())

then mapping each word to a pair of the word and a count of one:

    .map(lambda word: (word, 1))
    
and finally reducing the pairs by key using summation:

    .reduceByKey(lambda a,b : a + b)

### Word Count over Tweets ###

We can change the first actions on the RDD in the word count example and have it operate on tweet text.  The tweet data has been prepared with one
JSON tweet object per line in `2015-02-14.txt` and `2015-02-15.txt` (see Setup).  

The first lines look something like:

    lines.map(lambda line: json.loads(line)) \
         .flatMap(lambda tweet: tweet["text"].split()) 
         
which loads the JSON object and splits the "text" property instead of the whole line.

The code is in [tweet-wordcount.py](tweet-wordcount.py) and can be run by:

    $SPARK_HOME/bin/spark-submit tweet-wordcount.py "2015-02-*.txt"
    
### Understanding Scaling ###

By default, you are running Spark locally.  You can specify the "master" by the `--master` option which takes a URI.  

A special value of "local[n]" allows you to control the number of workers in your local cluster and can give you an
idea of "speed-up via parallelization" (within the limits of your hardware).

Try the following experiment:

    time $SPARK_HOME/bin/spark-submit --master local[1] wordcount.py "random-large-*.txt"
    
and note the time.  Now remove the `--master` option and do the same.  It should take longer as Spark will attempt
to guess and the correct number of local resources for your hardware.

Now, trying increasing `local[1]` to `local[2]` through `local[6]` and note the times.  Is there a limit to the 
increase in speed as you add more workers?

You can try the same experiments later by creating actual clusters of various sizes.  The only change would be
the value for the `--master` option.


## Activity - Problem Solving ##

The tweet data we prepared is from a conference.  How can we use Spark to answer the following questions?

 1. Who tweeted the most during the conference?
 2. What were the top 10 hash tags used?
 3. For a particular hour, how many tweets were produced?
 
## Activity - Deploying to Clusters ##

### Spark on EC2 ###

#### Overview ####

You can start a standalone Spark cluster on EC2 using the program `spark-ec2` located in the `ec2` directory of the spark distribution.  You'll need:

  * your key name
  * your local key (e.g. .pem file)
  * a preferred zone
  * your AWS key and secret
  
You'll need to setup two environment variables to contain your AWS credentials:

    export AWS_SECRET_ACCESS_KEY=xxxxxxxxx
    export AWS_ACCESS_KEY_ID=xxxxxxxx
    
You will need to make sure your access key is allowed to start EC2 instances.  You may need to modify the policy for the access key in "Identity and Access Management" and at minimum you'll
want:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Stmtnnnnnn",
                "Effect": "Allow",
                "Action": [
                    "ec2:*"
                ],
                "Resource": [
                     "*"
                ]
            }
        ]
    }
    
You can create this policy by clicking on "Create Another Policy" when viewing the group.  Use the policy generator and select "Amazon EC2" from the "AWS Service", 
select "All Actions" for "Actions", and enter "*" for "Amazon Resource Name (ARN)".  This is the most liberal policy and you can certain restrict it from there.
  
A simple cluster can then be launched as follows:

    $SPARK_HOME/ec2/spark-ec2 -k yourkey -i yourkey.pem -s 3 -t m3.medium -z us-east-1c --copy-aws-credentials launch "Spark Test"
   
At the very end you'll see the master hostname and you can visit this in your browser:

    http://ec2-nn-nn-nn-nn.compute-1.amazonaws.com:8080/
    
Spark jobs are run from the master node of the cluster.  You can login (ssh) via:

    $SPARK_HOME/ec2/spark-ec2 -k yourkey -i yourkey.pem login "Spark Test"
    
Finally, you can terminate your cluster:

    $SPARK_HOME/ec2/spark-ec2 -k yourkey -i yourkey.pem destroy "Spark Test"
    
Running a job requires two things:

  1. Your code (driver) must be transferred to the master node.
  2. Your data must be accessible by all nodes (copied to each node, put into HDFS or S3, etc.)

#### Testing ####

First let's try transferring our data and code to the master node:

    scp -i yourkey.pem wordcount.py root@ec2-nn-nn-nn-nn.compute-1.amazonaws.com:~
    scp -i yourkey.pem random/random-0.txt root@ec2-nn-nn-nn-nn.compute-1.amazonaws.com:~
   
Note: We'll only use the first set of random works to minimize network bandwidth use.

Then login:

    $SPARK_HOME/ec2/spark-ec2 -k yourkey -i yourkey.pem login "Spark Test"
   
Run a job:

    time spark/bin/spark-submit --master spark://ec2-nn-nn-nn-nn.compute-1.amazonaws.com:7077 wordcount.py random-0.txt > /dev/null
    
Now we can copy that same file to S3 from your local machine:

    aws s3 cp random/random-0.txt s3://mybucket/random/random-0.txt
    
and try the same job with an S3 URI (note the use of s3n)

    time spark/bin/spark-submit --master spark://ec2-nn-nn-nn-nn.compute-1.amazonaws.com:7077 wordcount.py s3n://mybucket/random/random-0.txt > /dev/null

You should see a notable difference in processing time as S3 is far slower than local files.

### Spark on EMR ###

TBD ... yarn, yarn, yarn
