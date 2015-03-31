# Creating Clusters for EMR #

## Setup ##

Install the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/) with 

    sudo pip install awscli

You may need to link to the executable:

    sudo ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/aws /opt/local/bin/aws
    
Then configure your system with the AWS key, secret, and default region (e.g. us-east-1).  You can leave the default output format blank.

    aws configure

You can re-run this command at any time to change the values.
    
Now you can test it by asking about your running EC2 instances (you may have none):

    aws ec2 describe-instances
    
You'll need two things to run any of the EMR activities:

   1. An S3 bucket to store logs, code, input, and output data.  
   2. An EMR cluster to run the examples.
    
## Basics of EMR Clusters ##
    
You can start a simple test cluster by doing the following:

    aws emr create-cluster --ami-version 3.4.0 --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.medium InstanceGroupType=CORE,InstanceCount=2,InstanceType=m1.medium --name "Test Cluster" --log-uri s3://mybucket/logs/ --enable-debugging --tags Name=emr
    
The --instance-groups option contains a set of triples in the shorthand syntax for `InstanceGroupType` (one of "MASTER", "CORE", or "TASK"), 
`InstanceType` (a EC2 instance type), and `InstanceCount` (the number of instances to start).  Alternatively, you can use JSON to describe the 
cluster instance groups.

For example, in a file [cluster.json](cluster.json):

    [
        {
          "InstanceGroupType": "MASTER",
          "InstanceCount": 1,
          "InstanceType": "m1.medium"
        },
        {
          "InstanceGroupType": "CORE",
          "InstanceCount": 2,
          "InstanceType": "m1.medium"
        }
    ]
    
and then the command:

    aws emr create-cluster --ami-version 3.4.0 --instance-groups file://./cluster.json --name "Test Cluster" --log-uri s3://mybucket/logs/ --enable-debugging --tags Name=emr

The command will return the "Cluster ID" that you will need for further manipulations including to terminating the cluster.  You can always find this via the command:

    aws emr list-clusters --active
    
You can terminate a cluster by:

    aws emr terminate-clusters --cluster-id <cluster-id>

The documentation examples consistently use the bucket name 'mybucket'.  You'll need to replace that with your bucket name to get the commands to work.

## Resizing a Cluster ##

You can add core or task nodes to a running cluster via the cluster details.  Clicking on "Resize" next to "Network and Hardware" will give you the ability to add Core and Task nodes
whilst choosing the instance type.  Clicking on "Resize" in the "Hardware" section only allows you to change the number of nodes of a given category with the same instance type.

Both of these are useful techniques to adjust your running cluster once you have found it to be insufficient for processing data.  The adjustment only happens after the currently 
running step completes.  As such, you may need to kill a running step if you know it will take too long to complete to adjust the size your running cluster.

## Bootstrap Actions ##

Once a generic cluster instance has been started, you may need to install specialized software (e.g. python packages).  You can specify a set of one-time actions 
called "Bootstrap Actions" when you create the cluster using the `--bootstrap-actions` option.  Like the --instance-groups option, you can use the shorthand syntax or JSON.

Each action must contain three things:

   * Path — the path to a script (typically in S3)
   * Args - any arguments to the script
   * Name — a name to show in the console
   
The shorthand is:

    --bootstrap-actions Path=s3://mybucket/python.sh,Name="Install python packages",Args=[numpy,nltk]
   
The JSON in `bootstrap.json`:

    [
       {
          "Path" : "s3://mybucket/python.sh",
          "Name" : "Install python packages",
          "Args" : ["numpy","nltk"]
       }
    ]
    
with the option:

    --bootstrap-actions file://./bootstrap.json
    
The script stored at s3://mybucket/python.sh might be something like:

    #!/bin/bash
    sudo pip install $*
    
### Testing Bootstrap Actions ###

In general, if you script runs on a like-operating system (e.g. linux of the same flavor), you'll be in good shape.  AWS EMR's AMI are based on RedHat/CentOS and 
so scripts that work on those particular flavors may work.  The right way to test bootstrapping is to use the specific AMI for the EMR version, start an EC2 
instance, and test on that machine.

### Testing Bootstrapping using EMR AMIs ###

You can test your bootstrapping commands by just starting the exact AMI used by EMR.  When you start a cluster, you can look up the 
AMI used by EMR in your EC2 console.  Under the details of a running or terminate instance associated with your cluster, you'll see
the AMI listed.  It should be a identifier formatted like "ami-xxxxxxxx".

For example, ami-2e88aa46 is the identifier for AMI version 3.6.0 that you can select when you start your cluster.  You can then
start an EC2 instance using that AMI using the CLI:

    aws ec2 run-instances --image-id ami-2e88aa46 --key-name your-key-name --instance-type m1.medium --placement AvailabilityZone=us-east-1c

In the above, you'll want to list your actual key name in place of `your-key-name` and adjust the `AvailabilityZone` value to your preference.
    
Now you can ssh into the machine using your key and the user `hadoop`.  This user has sudo privileges and so should be able to run your script exactly
as EMR would during cluster bootstrapping.

Once you are done, you can shutdown the instance via the console in the browser or use the instance ID returned from the `run-instances` command in the following:
   
    aws ec2 terminate-instances --instance-ids i-3259abcf    
    
## Running "Steps" ##

A step is a unit of work.  You add can steps to your cluster via the AWS CLI or via libraries like MRJob.

A step contains a set of jobs and a job contains a set of tasks (e.g. mappers and reducers).

Often, a single step contains a single job that contains a map/reduce process.  That map/reduce process is turned into a set of map tasks based on the input size.  The control over 
that process is handled by the input splitter used in Hadoop.  Subsequently, the number of reduce tasks depends on the number of map tasks.  These are all things you can control when you
configure Hadoop.
    
    
### Running Steps via AWS CLI ###

The AWS CLI command `aws emr add-steps` is used to add steps to your cluster.  The cluster identifier is necessary and you can find this in the cluster details.

The step is described by a set of metadata:

   * Name — A descriptive name.
   * Type — the type of Hadoop job (i.e. one of "CUSTOM_JAR", "STREAMING", "HIVE", "PIG", "IMPALA")
   * Args - a set of arguments to pass to the step
   * Jar — a location of a jar implementing the step (only for "CUSTOM_JAR").  This location must be accessible the Hadoop cluster and may be an S3 URI.
   * ActionOnFailure — One of "TERMINATE_CLUSTER", "CANCEL_AND_WAIT" (pause the step queue), "CONTINUE"
   * MainClass — the main class to use (only for CUSTOM_JAR)

The shorthand syntax can be used to specify all of the above but the JSON syntax is more useful:   

For example, a Hadoop streaming job might be specified as:
    
    [ {
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
    } ]
    
 The arguments are all specific to the [Hadoop Streaming program](http://hadoop.apache.org/docs/r2.6.0/hadoop-mapreduce-client/hadoop-mapreduce-client-core/HadoopStreaming.html).  Similarly,
 any other program would (including your own custom jar) would have its own argument definition.
 
 Once you have your JSON definition (`step.json` in this case), you can add it to your running cluster by:

    aws emr add-steps --cluster-id <your-id> --steps file://./step.json

### Running Steps via MRJob ###

[MRJob](http://mrjob.readthedocs.org) is a very useful abstraction and has the ability to run jobs directly on EMR.  While you can use MRJob to start a cluster,
a more useful technique is to run your MRJob program on an already started cluster.  

Running on an existing cluster is easily done by two extra parameters:

   1. Add the `-r emr` option to select the EMR runner.
   2. Add the `--emr-job-flow-id your-cluster-id` to specify your existing cluster.
   
Since you are running on the cluster, there are some additional life-cycle options you may want to control.  First, by default, MRJob will upload your
input (e.g. stdin) to S3 and download the output.  You'll probably want to run everything from S3 and this is easily done:

   1. Specify your input bucket by just an extra argument to your program just as you might give it a file name but instead just give in the S3 bucket URI.
   2. Use `--no-output` to turn off downloading the result and `--output-dir s3://yourbucket/yourpath` to specify the output S3 bucket.

If you have supporting code for your program, you'll need to package it into an archive in tar/gz format.  Then just specify that on the command-line using `--python-archive code.tar.gz`
   
You may have changed the version of python on your cluster via a bootstrap action.  If so, you can specify the python command via `--python-bin`.  That command expects a command (or full path)
that will run the python interpreter.

When you use the `--no-output` and `--output-dir` together with MRJob the results are stored on AWS S3.  You can interrupt the local MRJob process after the step has started 
and it will continue to run on your cluster.  This allows you to terminate the local process and continue other work.  You will have to check the cluster interface online to
see the status of your job.

### Killing Steps ###

There is no easy way to kill a running step via the AWS CLI or the browser interface.  If you terminate the cluster, the step will be killed first but that is a 
draconian way to kill a step.  If you stop the cluster, you will have restart the cluster and that can take quite awhile.

The way you kill the step is to talk to Hadoop directly by the following:

  1. SSH into the master node.  You'll find the connection information in the cluster details and then you'll do something like:
  
    `ssh hadoop@ec2-nn-nn-nn-nn.compute-1.amazonaws.com -i ~/your-identity.pem`
      
  2. Once you are connected, list the jobs with `mapred job -list`
  
  3. Locate the row that represents the step you'd like to kill.  At this point, a step has turned into a set of jobs.  If you only have one job, there will be only one row.
  
  4. The first column is labeled `JobId`.  Use that identifier to kill the job with `mapred job -kill id` where `id` is the value in that column.  
    
## Manipulating S3 Buckets via AWS CLI ##

You can create a bucket by:

    aws s3 mb s3://mybucket/

Listing a bucket:

    aws s3 ls s3://mybucket/
    
Copying a file to a path:

    aws s3 cp file.txt s3://mybucket/somewhere/
    
Removing a key:

    aws s3 rm s3://mybucket/somewhere/file.txt

Syncing a directory to s3 (both ways):

    aws s3 sync somewhere s3://mybucket/somewhere
    aws s3 sync s3://mybucket/somewhere somewhere
    

Removing a set of keys via a prefix:

    aws s3 rm s3://mybucket/somewhere/ --recursive
