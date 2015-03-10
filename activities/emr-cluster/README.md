# SETUP #

Install the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/) with 

    sudo pip install awscli

You may need to link to the executable:

    sudo ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/aws /opt/local/bin/aws
    
Then configure your system with the AWS key, secret, and default region (e.g. us-east-1).  You can leave the default output format blank.

    aws configure

You can re-run this command at any time to change the values.
    
Now you can test it by asking about your running EC2 instances (you may have none):

    aws ec2 describe-instances
    
You'll need two things to run any of the demos:

   1. An S3 bucket to store logs, code, input, and output data.  
   2. An EMR cluster to run the examples.

You can start a simple test cluster by doing the following:

    aws emr create-cluster --ami-version 3.4.0 --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.medium InstanceGroupType=CORE,InstanceCount=2,InstanceType=m1.medium --name "Test Cluster" --log-uri s3://mybucket/logs/ --enable-debugging --tags Name=emr

The command will return the "Cluster ID" that you will need for further manipulations including to terminating the cluster.  You can always find this via the command:

    aws emr list-clusters --active
    
You can terminate a cluster by:

    aws emr terminate-clusters --cluster-id <cluster-id>

The documentation examples consistently use the bucket name 'mybucket'.  You'll need to replace that with your bucket name to get the commands to work.

You can create a bucket by:

    aws s3 mb s3://mybucket/

You should be familiar with how to use S3 via this tool:

    aws s3 ls s3://mybucket/
    aws s3 cp file.txt s3://mybucket/
    aws s3 rm s3://mybucket/file.txt
    aws s3 sync dir s3://mybucket/dir
    aws s3 sync s3://mybucket/dir dir
    aws s3 rm s3://mybucket/dir --recursive
