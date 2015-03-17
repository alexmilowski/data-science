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
