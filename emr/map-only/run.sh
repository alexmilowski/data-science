#!/bin/bash
EMRCLI=~/workspace/elastic-mapreduce-ruby/elastic-mapreduce
JOBFLOW=$1
BUCKET=$2
INPUT=$3
OUTPUT=$4
$EMRCLI --jobflow $JOBFLOW --jar /home/hadoop/contrib/streaming/hadoop-streaming.jar --args "-files,s3://$BUCKET/line-count.py,-mapper,line-count.py,-reducer,NONE,-input,s3://$BUCKET/$INPUT/,-output,s3://$BUCKET/$OUTPUT/" --step-name "Line Count (Map Only)"

