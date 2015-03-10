# Map Task Input Splitting #

This example shows how map tasks get their input from splitting the input files.  In this example, we'll 
just count the lines received via a map-only step (i.e., no reduce step) and the output will just consist
of that count.  You'll see the output of each map task and how much of the input it received.

# Setup #

If you don't have a cluster running, you'll need to start one (see main setup page).  You also need a bucket for the code, input, and output.

# Running the Example #

## Step 1 ##
    
You'll need to setup input to run the job and so we'll create a directory with some input:

    mkdir -p job/input
    python generate-input.py job/input/test 3 1000
    
This will create three test files. We will process this with a simple map-only task to show you how input 
is split. 

Now we need to store the input:

    aws s3 sync job s3://mybucket/job/
    
## Step 2 ##

We need to store the line count program:

    aws s3 cp line-count.py s3://mybucket/
    
## Step 3 ##
    
Now we add the streaming step to do the work:

    aws emr add-steps --cluster-id <your-id> --steps Type=STREAMING,Name='Map Line Count',ActionOnFailure=CONTINUE,Args=--files,s3://mybucket/line-count.py,-mapper,line-count.py,-reducer,NONE,-input,s3://mybucket/job/input,-output,s3://mybucket/job/output

Note: don't forget to use your cluster id and bucket name in the above.

This command returns the step id that you can use for further monitoring.  If you use an 'm1.medium' instance type, this job should take 1 minute to process and 3 minutes of elapsed time.

You can monitor its progress from the console or via:

    aws emr describe-step --cluster-id <cluster-id> --step-id <step-id>

## Step 4 ##

Sync the output:

   aws s3 sync s3://mybucket/job/output/ job/output/   

You should now have 7 files:

    job/output/_SUCCESS
    job/output/part-00000
    job/output/part-00001
    job/output/part-00002
    job/output/part-00003
    job/output/part-00004
    job/output/part-00005

