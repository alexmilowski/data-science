#!/bin/bash
if [ -z $1 ] || [ -z $2 ]; then
   echo "Usage: $(basename $0) key-name bucket-name"
   exit 1
fi
tmpname="/tmp/$(basename $0).bootstrap.$$.json"
echo "[{\"Path\" : \"s3://$2/cc-bootstrap.sh\", \"Name\" : \"Common Crawl Bootstrap\", \"Args\" : [] }, { \"Path\":\"s3://elasticmapreduce/bootstrap-actions/configure-hadoop\",\"Args\":[\"-m\",\"mapred.map.max.attempts=1\"]} ]" > $tmpname

AMI_VERSION=3.6.0
CLUSTER=file://./cluster.json
LOG_PATH=logs/
TAG=emr

aws emr create-cluster --ami-version $AMI_VERSION --ec2-attributes KeyName=$1 --instance-groups $CLUSTER --name "Crawl The Crawl Cluster" --log-uri s3://$2/$LOG_PATH --enable-debugging --tags Name=$TAG --bootstrap-actions file://$tmpname --applications "[]"
rm -f $tmpname