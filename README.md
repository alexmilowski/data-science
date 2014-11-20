![Common Crawl Logo](http://commoncrawl.org/wp-content/uploads/2012/04/ccLogo.png)

# mrjob starter kit

This project demonstrates using Python to process the Common Crawl dataset with the mrjob framework.
There are three tasks to run using the three different data formats:

+ Counting HTML tags using Common Crawl's raw response data (WARC files)
+ Analysis of web servers using Common Crawl's metadata (WAT files)
+ Word count using Common Crawl's extract text (WET files)

In addition, there is a more complex version of the server analysis tool that will only count unique domains.
This provides a good example of a more complex MapReduce job that involves an additional reduce step.

## Setup

To develop locally, you will need to install the `mrjob` Hadoop streaming framework, the `boto` library for AWS, the `warc` library for accessing the web data, and `gzipstream` to allow Python stream decompress gzip files.

This can all be done using `pip`:

    pip install -r requirements.txt

If you would like to create a virtual environment to protect local dependencies:

    virtualenv --no-site-packages env/
    source env/bin/activate
    pip install -r requirements.txt

To develop locally, you'll need at least three data files -- one for each format the crawl uses.
These can either be downloaded by running the `get-data.sh` command line program or manually by grabbing the [WARC](https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/warc/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.gz), [WAT](https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wat/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wat.gz), and [WET](https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/wet/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc.wet.gz) files.

## Running the code

The example code includes three tasks, the first of which runs a HTML tag counter over the raw web data.
One could use it to see how well HTML5 is being adopted or to see how strangely people use heading tags.

    "h1" 520487
    "h2" 1444041
    "h3" 1958891
    "h4" 1149127
    "h5" 368755
    "h6" 245941
    "h7" 1043
    "h8" 29
    "h10" 3
    "h11" 5
    "h12" 3
    "h13" 4
    "h14" 19
    "h15" 5
    "h21" 1

We'll be using `tag_counter.py` as our primary task, which runs over WARC files.
To run the other examples, `server_analysis.py` (WAT) or `word_count.py` (WET), simply run that Python script whilst using the relevant input format.

### Running locally

Running the code locally is made incredibly simple thanks to mrjob.
Developing and testing your code doesn't actually need a Hadoop installation.

First, you'll need to get the relevant demo data locally, which can be done by running:

    ./get-data.sh
    
If you're on Windows, you just need to download the files listed and place them in the appropriate folders.

To run the jobs locally, you can simply run:

    # we need to turn the relative paths in the input files into absolute paths before passing them to mrjob§
    python absolutize_path.py < input/test-1.warc | python tag_counter.py --conf-path mrjob.conf --no-output --output-dir out
    
    # or 'local' simulates more features of Hadoop such as counters
    python absolutize_path.py < input/test-1.warc | python tag_counter.py -r local --conf-path mrjob.conf --no-output --output-dir out

### Running via Elastic MapReduce

As the Common Crawl dataset lives in the Amazon Public Datasets program, you can access and process it without incurring any transfer costs.
The only cost that you incur is the cost of the machines and Elastic MapReduce itself.

By default, EMR machines run with Python 2.6.
The configuration file automatically installs Python 2.7 on your cluster for you.
The steps to do this are documented in `mrjob.conf`.

To run the job on Amazon Elastic MapReduce (their automated Hadoop cluster offering), you need to add your AWS access key ID and AWS access key to `mrjob.conf`.
By default, the configuration file only launches two machines, both using spot instances to be cost effective.

    python tag_counter.py -r emr --conf-path mrjob.conf --no-output --output-dir out input/test-100.warc

If you are running this for a full fledged job, you will likely want to make the master server a normal instance, as spot instances can disappear at any time.

## Running it over all of Common Crawl

To run your mrjob task over the entirety of the Common Crawl dataset, you can use the WARC, WAT, or WET file listings found at `CC-MAIN-YYYY-WW/[warc|wat|wet].paths.gz`.

As an example, the [August 2014 crawl](http://commoncrawl.org/august-2014-crawl-data-available/) has 52,849 WARC files listed by [warc.paths.gz](https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-35/warc.paths.gz).

It is highly recommended to run over batches of files at a time and then perform a secondary reduce over those results.
Running a single job over the entirety of the dataset complicates the situation substantially.
We also recommend having [N map jobs for the N files](https://groups.google.com/forum/#!topic/mrjob/o9t5FrgkMCs) you'll be attempting such that if there is a transient error, the minimal amount of work will be lost.

You'll also want to place your results in an S3 bucket instead of having them streamed back to your local machine.
For full details on this, refer to the mrjob documentation.

## Running with PyPy

If you're interested in using PyPy for a speed boost, you can look at the [source code](https://github.com/mcroydon/social-graph-analysis) from **Social Graph Analysis using Elastic MapReduce and PyPy**.

## License

MIT License, as per `LICENSE`
