#!/bin/bash

sudo yum install -y python27 python27-devel python27-pip gcc-c++
sudo pip-2.7 install boto mrjob warc
sudo pip-2.7 install https://github.com/commoncrawl/gzipstream/archive/master.zip
