#!/bin/bash

# This script expects the path list as input for the MRJob

SCRIPT=$1
BUCKET=$2
FLOWID=$3

if [ -z $SCRIPT  ] || [ -z $BUCKET  ] || [ -z $FLOWID ] ; then
   echo "Usage: $(basename $0) script.py bucket-name job-flow-id"
   exit 1
fi

shift 3
OUTDIR=s3://$BUCKET/common-crawl/wat/domains/$$
echo "Output: $OUTDIR"
python $SCRIPT -r emr --python-bin python2.7 --python-archive mrcc.tar.gz --no-output --output-dir $OUTDIR --emr-job-flow-id $FLOWID $*
