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
    
    
## Note on S3 Buckets ##

You can create a bucket by:

    aws s3 mb s3://mybucket/

You should be familiar with how to use S3 via this tool:

    aws s3 ls s3://mybucket/
    aws s3 cp file.txt s3://mybucket/
    aws s3 rm s3://mybucket/file.txt
    aws s3 sync dir s3://mybucket/dir
    aws s3 sync s3://mybucket/dir dir
    aws s3 rm s3://mybucket/dir --recursive
