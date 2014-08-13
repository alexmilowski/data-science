![Common Crawl Logo](http://commoncrawl.org/wp-content/uploads/2012/04/ccLogo.png)

# Common Crawl mrjob starter kit

This project demonstrates using the Common Crawl dataset with the mrjob framework.

# Running the jobs

To develop locally, you will need to install the `mrjob` Hadoop streaming framework, the `boto` library for AWS, the `warc` library for accessing the web data, and `gzipstream` to allow Python stream decompress gzip files.

This can all be done using `pip`:

    pip install -r requirements.txt

If you would like to create a virtual environment to protect local dependencies:

    virtualenv --no-site-packages env/
    source env/bin/activate
    pip install -r requirements.txt

To run the jobs locally, you can simply run:

    python mrcc.py --conf-path mrjob.conf --no-output --output-dir out test-1.txt
    # or 'local' simulates more features of Hadoop
    python mrcc.py -r local --conf-path mrjob.conf --no-output --output-dir out test-10.txt

Note: the jobs stream the web data from Amazon S3.
This means if you use it locally, your computer will be downloading approximately a gigabyte per file.

To run the job on Amazon Elastic MapReduce (their automated Hadoop cluster offering), you need to add your AWS access key ID and AWS access key to `mrjob.conf`.

    python mrcc.py -r emr --conf-path mrjob.conf --no-output --output-dir out test-10.txt

# License

MIT License, as per `LICENSE`
