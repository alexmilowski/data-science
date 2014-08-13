![Common Crawl Logo](http://commoncrawl.org/wp-content/uploads/2012/04/ccLogo.png)

# mrjob starter kit

This project demonstrates using Python to process the Common Crawl dataset with the mrjob framework.
The first task we show counts HTML tag usage across the web.

## Setup

To develop locally, you will need to install the `mrjob` Hadoop streaming framework, the `boto` library for AWS, the `warc` library for accessing the web data, and `gzipstream` to allow Python stream decompress gzip files.

This can all be done using `pip`:

    pip install -r requirements.txt

If you would like to create a virtual environment to protect local dependencies:

    virtualenv --no-site-packages env/
    source env/bin/activate
    pip install -r requirements.txt

## Running the code

The example code included runs a HTML tag counter over the raw web data.
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

### Running locally

Running the code locally is made incredibly simple thanks to mrjob.
Developing and testing your code doesn't actually need a Hadoop installation.

To run the jobs locally, you can simply run:

    python mrcc.py --conf-path mrjob.conf --no-output --output-dir out input/test-1.txt
    # or 'local' simulates more features of Hadoop
    python mrcc.py -r local --conf-path mrjob.conf --no-output --output-dir out input/test-1.txt

*Note:* the jobs stream the web data from Amazon S3.
This means if you use it locally, your computer will be downloading approximately a gigabyte per file.

### Running via Elastic MapReduce

As the Common Crawl dataset lives in the Amazon Public Datasets program, you can access and process it without incurring any transfer costs.
The only cost that you incur is the cost of the machines and Elastic MapReduce itself.

By default, EMR machines run with Python 2.6.
The configuration file automatically installs Python 2.7 on your cluster for you.
The steps are documented in `mrjob.conf`.

To run the job on Amazon Elastic MapReduce (their automated Hadoop cluster offering), you need to add your AWS access key ID and AWS access key to `mrjob.conf`.
By default, the configuration file only launches two machines, both using spot instances to save money.

    python mrcc.py -r emr --conf-path mrjob.conf --no-output --output-dir out input/test-100.txt

If you are running this for a full fledged job, you will likely want to make the master server a normal instance, as spot instances can disappear at any time.

## Running it over all Common Crawl

To run your mrjob task over the entirety of the Common Crawl dataset, you can use download the WARC file listing found at `CC-MAIN-YYYY-WW/warc.paths.gz`.

As an example, the [July 2014 crawl](http://commoncrawl.org/july-2014-crawl-data-available/) has 63,560 WARC files listed by [warc.paths.gz](https://aws-publicdatasets.s3.amazonaws.com/common-crawl/crawl-data/CC-MAIN-2014-23/warc.path.gz).

It is highly recommended to run over batches of WARC files at a time and then perform a secondary reduce over those results.
Running a single job over the entirety of the dataset complicates the situation substantially.

## Running with PyPy

If you're interested in using PyPy for a speed boost, you can look at the [source code](https://github.com/mcroydon/social-graph-analysis) from **Social Graph Analysis using Elastic MapReduce and PyPy**.

## License

MIT License, as per `LICENSE`
