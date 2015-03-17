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
    
This should take about x minutes.

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
   

