#!/bin/bash
EMRCLI=~/workspace/elastic-mapreduce-ruby/elastic-mapreduce
JOBFLOW=$1
BUCKET=$2
INPUT=$3
OUTPUT=$4
$EMRCLI --jobflow $JOBFLOW --jar /home/hadoop/contrib/streaming/hadoop-streaming.jar --args "-files,s3://$BUCKET/prime-factors.py,-mapper,prime-factors.py,-reducer,aggregate,-input,s3://$BUCKET/$INPUT/,-output,s3://$BUCKET/$OUTPUT/" --step-name "Multiply"

