
# Word Counts for Tweets #

This example shows running the word count example over tweets.

# Setup #

If you don't have a cluster running, you'll need to start one (see main setup page).  You also need a bucket for the code, input, and output.

# Running the Example #

In this example, we'll use a sample set of 1995 tweets with the word 'Microsoft' in them.

## Step 1 ##

The tweets are stored as JSON and We'll need to extract the tweet text and create an input with one line per tweet.  The `format-tweets.py` program
does this:

    mkdir -p tweet-wc/input
    python format-tweets.py microsoft-2014-10-07.json > tweet-wc/input/tweets.txt
    
Now we need to store the input:

    aws s3 sync tweet-wc s3://mybucket/tweet-wc/

## Step 2 ##

We need to store the word count program:

    aws s3 cp tweetSplitter.py s3://mybucket/
        
## Step 3 ##

Now we add the streaming step to do the work:

    aws emr add-steps --cluster-id <your-id> --steps Type=STREAMING,Name='Tweet Word Count',ActionOnFailure=CONTINUE,Args=--files,s3://mybucket/tweetSplitter.py,-mapper,tweetSplitter.py,-reducer,aggregate,-input,s3://mybucket/tweet-wc/input,-output,s3://mybucket/tweet-wc/output

Note: don't forget to use your cluster id and bucket name in the above.

This command returns the step id that you can use for further monitoring.  If you use an 'm1.medium' instance type, this job should take 1 minute to process and 3 minutes of elapsed time.

You can monitor its progress from the console or via:

    aws emr describe-step --cluster-id <cluster-id> --step-id <step-id>
    
## Step 4 ##

Sync the output:

   aws s3 sync s3://mybucket/tweet-wc/output/ tweet-wc/output/
   
You should now have 4 files:

    tweet-wc/output/_SUCCESS
    tweet-wc/output/part-00000
    tweet-wc/output/part-00001
    tweet-wc/output/part-00002
    
The output is a list of primes and exponents for a very large number!
