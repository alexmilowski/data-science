# Processing the NASA OpenNEX model in EMR #

NASA produced a climate model which has been made available as web resources via the PAN methodology at
as an example at http://data.pantabular.org/opennex/ with a demonstration application at http://data.pantabular.org/opennex/explore/

In this activity, we will be using this climate model data as an example data set to process numerical information in MRJob
and produce various averages and summaries.

## Acquiring the Data ##

To begin with, we will run the Map/Reduce processes locally on a data set rather than off S3 and via EMR.  All of the 
examples can easily be translated by storing data in S3 and using the EMR runner to deploy the MRJob code on a cluster.

The file [acquire.py](acquire.py) is a program that will download the data in PAN format and output the data as JSON
data files.  The program has the arguments:

   * the data set name
   * a resolution counts of a 1/120° 
   * a quadrangle in JSON array syntax
   * a start year/month (e.g., 2015-03)
   * an end year/month
   * an output directory
   
For example:

    python acquire.py avg-rcp85 60 "[40,-125,35,-120]" 2015-03 2015-03 dataset/
    
downloads data for the month of March, 2015 for 0.5° partitions for the data set `avg-rcp85` and stores it into the directory `dataset/`.

The output is a set of files based on sequence numbers that cover the requested geospatial region.  They are named `{year}-{month}-{resolution}-{sequence#}.json` and 
stored directory given as one JSON object per file without newlines in the formatting.

For this activity, acquire the first three months of data for 2015:

    python acquire.py avg-rcp85 60 "[40,-125,35,-120]" 2015-01 2015-03 dataset/
    
This should take about 2-3 minutes.

## Understanding the Data ##

The JSON object has the format:

    {
        "data" : [ 286.19, 286.19, 286.18, ... ],
        "yearMonth" : "2015-01", 
        "sequence": 74634, 
        "resolution": 60, 
        "dataset": "avg-rcp85"
    }
    
The array value for "data" is a set of temperature values in Kelvins from the model associated with the geospatial region for the sequence number.

## Supporting Code ##

There are two supporting libraries:

   * seqs.py — a library supporting generating sequence numbers from latitude/longitude
   * date_partitions — a library supporting generating sequences of dates for partitioning time

A set of sequence numbers given geospatial region can be enumerated giving the quadrangle and the size (in degrees):

    seqs.sequencesFromQuadrangle(0.5,[40,-125,35,-120])
    
where `0.5` is for half-degree quadrangles covering the region defined by the two points (40°,-125°) and (35°,-120°).

The two supporting libraries can be put together:

    import datetime
    import seqs
    import date_partitions as partitions

    for month in partitions.month_partition(datetime.datetime(2015,3,1),datetime.datetime(2015,5,1)):
       for seq in seqs.sequencesFromQuadrangle(0.5,[40,-125,35,-120]):
          print "{}-{:02d},{}".format(month.year,month.month,seq)
   
## Input Example ##

Because we'll be running the example locally, we can just create input from each of the data files where each line contains a single 
JSON object.  The example code [input-example.py](input-example.py) produces an average via map/reduce (mrjob) over the data loaded.

To run the example on the first three months we acquired:

    cat dataset/2015-0[1-3]*.json | python input-example.py
    
The mapper loads the data from the line given and computes an average:

    def mapper(self, _, line):
       obj = json.loads(line)
       yield "average",sum(obj["data"])/len(obj["data"])

## Average Example ##

A more complicated example in [average.py](average.py) computes an average by month and keeps track of the counts.  It uses a combiner
to collect the sequence numbers associated with the month and then does the reduce step to compute the overall average.  It uses the 
counts to make sure the average is calculated correctly.

To run the example on the first three months we acquired:

    cat dataset/2015-0[1-3]*.json | python average.py
    
Note that the average is not quite the same.

## Activity ##

We'd like to take these simple examples and compute over a more generic input.  We can transition our code to run over a local dataset (or one in S3)
by using a setup like [by-sequences.py] where the data is retrieved from a data set and the input is a specification of what to process.

This program assumes input in a CSV format with the columns:

   * lat1 — the NW latitude of the quadrangle
   * lon1 — the NW longitude of the quadrangle
   * lat2 — the SE latitude of the quadrangle
   * lon2 — the SE longitude of the quadrangle
   * size — the count of 1/120° arc lengths of the resolution (usually 60)
   * startYear - the year to start
   * startMonth - the month to start
   * endYear — the year to end
   * endMonth — the month to end
   
An input might look like:

    #lat1,lon1,lat2,lon2,size,startYear,startMonth,endYear,endMonth
    40,-125,35,-120,60,2015,02,2015,03
    
and you can run the sample code like:

    python by-sequences.py --data-dir `pwd`/dataset/ < input-sequences.txt
    
The sample code is a two-step map/reduce job.  Your task is to modify it so that it correcly computes an average for the given input line.  Take a look 
at `average.py` and see how you might modify the various methods and add/replace them in `by-sequences.py`.

