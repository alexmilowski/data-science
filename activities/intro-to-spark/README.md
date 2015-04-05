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

### Preparing Sample Data ###

We'll be using the same conference data from the [Organzing Acquired Data](../../assignments/organizing-tweets/) assignment.  We will prepare the data by writing each tweet onto a single line:

    python one-line-json.py < ../../assignments/organizing-tweets/prague-2015-02-14.json > 2015-02-14.txt
    python one-line-json.py < ../../assignments/organizing-tweets/prague-2015-02-15.json > 2015-02-15.txt
        
We'll also use some randomly generated files:

    curl "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain" > words
    python random-text.py 10000 100 < words > random-0.txt
    python random-text.py 10000 100 < words > random-1.txt
    python random-text.py 10000 100 < words > random-2.txt
    python random-text.py 10000 100 < words > random-3.txt
    python random-text.py 10000 100 < words > random-4.txt
    python random-text.py 10000 100 < words > random-5.txt
    python random-text.py 10000 100 < words > random-6.txt
    python random-text.py 10000 100 < words > random-7.txt
    python random-text.py 10000 100 < words > random-8.txt
    python random-text.py 10000 100 < words > random-9.txt
    


## Activity - Running some example ##


    