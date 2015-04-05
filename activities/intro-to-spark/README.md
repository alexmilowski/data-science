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
    python random-text.py 1000000 10 < words > random-0.txt
    python random-text.py 1000000 10 < words > random-1.txt
    python random-text.py 1000000 10 < words > random-2.txt
    python random-text.py 1000000 10 < words > random-3.txt
    python random-text.py 1000000 10 < words > random-4.txt
    python random-text.py 1000000 10 < words > random-5.txt
    python random-text.py 1000000 10 < words > random-6.txt
    python random-text.py 1000000 10 < words > random-7.txt
    python random-text.py 1000000 10 < words > random-8.txt
    python random-text.py 1000000 10 < words > random-9.txt


## Activity - Run some example ##

### Hello World - Word Count ###

The classic "hello world" of map/reduce is a simple word count.  An example implementation is in [wordcount.py](wordcount.py) and can be run as follows:

    $SPARK_HOME/bin/spark-submit wordcount.py "random-large-*.txt"
    
This will run the word count over the randomly generated data (from the setup) of 100 million words.

The RDD contains a wild card and is effectively the same as:

    lines = sc.textFile("random-large-*.txt", 1)
    
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

### Spark on EMR ###
