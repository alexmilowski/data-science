# Multiplying Many Integers via Prime Factorization using EMR#

This example demonstrates how map reduce key/values work by mulitplying a large
number of integers.  In this case, the output keys are prime numbers and the value is
the exponent of the prime factorization (e.g. 12 produces 2 → 2, 3 → 1).

It also uses the built-in aggregator as the reducer step and so the output is prefixes with `LongValueSum:`.

## Setup ##

If you don't have a cluster running, you'll need to start one (see main setup page).  You also need a bucket for the code, input, and output.

## Running the Example ##

In this example, we'll multiple 1,000,000 integers between 1 and 1000

### Step 1 ###

You'll need to setup input to run the job and so we'll create a directory with some input:

    mkdir -p multiply/input
    python generate-input.py 1000 1000000 > multiply/input/numbers.txt
    
Now we need to store the input:

    aws s3 sync multiply s3://mybucket/multiply/

### Step 2 ###

We need to store the line count program:

    aws s3 cp prime-factors.py s3://mybucket/
    
### Step 3 ###
    
Now we add the streaming step to do the work (shorthand)

    aws emr add-steps --cluster-id <your-id> --steps Type=STREAMING,Name='Multiply',ActionOnFailure=CONTINUE,Args=--files,s3://mybucket/prime-factors.py,-mapper,prime-factors.py,-reducer,aggregate,-input,s3://mybucket/multiply/input,-output,s3://mybucket/multiply/output

or using JSON:

    aws emr add-steps --cluster-id <your-id> --steps file://./step.json
    
where `step.json` is:
    
    {
       "Type" : "STREAMING",
       "Name" : "Multiply",
       "ActionOnFailure" : "CONTINUE",
       "Args" : [
          "-files","s3://mybucket/prime-factors.py",
          "-mapper","prime-factors.py",
          "-reducer","aggregate",
          "-input","s3://mybucket/multiply/input",
          "-output","s3://mybucket/multiply/output"
       ]
    }
    
Note: don't forget to use your cluster id and bucket name in the above.

This command returns the step id that you can use for further monitoring.  If you use an 'm1.medium' instance type, this job should take 1 minute to process and 2 minutes of elapsed time.

You can monitor its progress from the console or via:

    aws emr describe-step --cluster-id <cluster-id> --step-id <step-id>
    
### Step 4 ###

Sync the output:

    aws s3 sync s3://mybucket/multiply/output/multiply/output/
   
You should now have 4 files:

    job/output/_SUCCESS
    job/output/part-00000
    job/output/part-00001
    job/output/part-00002
    
The output is a list of primes and exponents for a very large number!
