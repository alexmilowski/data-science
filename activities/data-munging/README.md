# Data Munging - Processing JSON, XML, and CSV Data #

## CWOP Data Set ##

The Citizen Weather Observation Program (CWOP) collects weather data from a variety of citizen, business, and government 
sources over the Internet.  It collects over 75,000 weather reports an hour from 10,000+ weather stations located all over
the world but mostly concentrated in North America.

The data collected is transmitted in as APRS weather reports (need ref) in a coded format that is eventually disseminated
via a real-time peer-to-peer network using a system called APRS-IS (need ref).  This information can be received and decoded
by attaching to a several of the servers associated with the CWOP program and aggregated the results.

The [mesonet.info](http://www.mesonet.info) collects and aggregates this data.  The data acquisition process first
serializes the data collected from each server into 5 minute segments stored in an custom XML format:

    <aprs xmlns="http://weather.milowski.com/V/APRS/" source="cwop1" start="2014-12-26T00:05:00Z">
    <report from="EW4197" type="weather" latitude="37.28667" longitude="-118.38833" received="2014-12-26T00:05:00Z" at="2014-12-26T00:05:00Z" wind-dir="334" wind-speed="10" wind-gust="22" temperature="38" rain-hour="0" rain-24hours="0" rain-midnight="0" humidity="27" pressure="10139" />
    <report from="EW5868" type="weather" latitude="39.69333" longitude="-91.04283" received="2014-12-26T00:05:00Z" at="2014-12-26T00:05:00Z" wind-dir="150" wind-speed="4" wind-gust="11" temperature="43" rain-hour="0" rain-24hours="1" rain-midnight="1" humidity="67" pressure="10118" />
    <report from="KA9EES" type="weather" latitude="40.11117" longitude="-87.8725" received="2014-12-26T00:05:00Z" at="2014-12-26T00:05:00Z" wind-dir="152" wind-speed="6" wind-gust="12" temperature="39" rain-hour="0" rain-24hours="0" rain-midnight="0" pressure="10165" />
    ...
    </aprs>
    
Each weather report has an identifier (@from), a location (@latitude and @longitude), a received time (@received), a generation time from the weather station (@at), and a 
variety of weather report facets (e.g., @temperature).  These facets for the weather reports and their units of measure are listed below:

wind-dir
wind-speed
wind-gust
temperature
rain-hour
rain-24hours
rain-midnight
humidity
pressure

An excerpt of this data for 2014-12-26 has been stored on AWS S3 in the public bucket `milowski-cwop-data`.  It is organized first by date (e.g., 2014-12-26) and then by format and hour.  The
raw XML data has been transformed into JSON (geo JSON?) and CSV data formats as well.  Each of the variations are located on 'xml', 'json', or 'csv' "directories" in S3.  

For example, 2014-12-26 from 13:00 to 14:00 in JSON is located in:

   s3://milowski-cwop-data/2014-12-26/json/13:00/

Each key (file) in represents a 5 minute segment of data partitioned only by time.  The location of the reports can only be sorted by selecting the subset of information 
amongst all the various sources stored under the same key (directory).

For example, you'll find the full keys for the data set as follows:

    s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop1-2014-12-26T13:00:00Z.json
    s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop1-2014-12-26T13:05:00Z.json
    s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop1-2014-12-26T13:10:00Z.json
    ...
    s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop2-2014-12-26T13:00:00Z.json
    s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop2-2014-12-26T13:05:00Z.json
    s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop2-2014-12-26T13:10:00Z.json
    ...

The names of the keys encode the source server and start of the time segment.  This information is only repeated in the XML source and not in the JSON or CSV formats.

## Activities ##

In this activity, we will be:

   * downloading copies of the data via S3
   * processing a variety of data formats (i.e., XML, JSON, and CSV)
   * computing simple statistics or subsets
   * accessing data directly via S3 via boto
   
In general, we'll be computing two things:

   * an average (e.g., average temperature)
   * geospatial subsets for rectangular areas (quadrangles)

### A. Making a Copy ###

#### Description ####

The data is available on S3 and you can download a copy (or a subset) easily via the AWS CLI.  Keep in mind that S3 is a key/value store.  All the data is associated with 
the full path of the key.  The concept of a "directory" and contained "files" is only implied by the "/" in the key and so is an interpretation of the tool being used.

Fortunately, the AWS CLI interprets directories in keys as you might expect.  Try the following:

    aws s3 ls s3://milowski-cwop-data/2014-12-26/json/13:00/

When you run that command, you should see the complete listing of 79 keys (files).

You can copy a single file or directory to your local drive via the same base command.  To copy a file locally, try:

    aws s3 cp s3://milowski-cwop-data/2014-12-26/json/13:00/weather-cwop1-2014-12-26T13:00:00Z.json .
    
If you want to copy a whole directory, try:

    aws s3 cp s3://milowski-cwop-data/2014-12-26/json/13:00 . --recursive
        
#### Tasks ####

  1. Pick an particular hour (e.g., 13:00)
  2. Copy the remote buckets for all the formats (i.e., 'xml', 'json', 'csv') to your local disk.
  
  
### B. Parsing XML: Computing an Average ###

#### Description ####

In this activity you'll be parsing XML data sources and computing an average temperature.  You will want to iterate a set of XML documents in a directory, parsing each XML source,
and interpret the @temperature attribute as a real number measuring temperature in Fahrenheit.  You should compute an average over all weather reports in all the documents you process.

You can parse XML using Python's built in [xml.etree module](https://docs.python.org/2/library/xml.etree.elementtree.html); see [xml-parse.py](xml-parse.py).

#### Tasks ####

   1. Pick a particular hour.
   2. Parse all the XML files in python and sum the temperature values for every observed weather report.
   3. Calculate the average temperature for that hour for all the CWOP data received.

### C. Parsing JSON: Geospatial Partitioning ###

#### Description ####

The CWOP XML data has been translated into [geojson](http://geojson.org).  The data is received in whatever order the weather stations report them but it can be filter for a specific region.
We'll parse the weather data as JSON and select only those that occur within a specific quadrangle.

#### Tasks ####

   1. Pick a particular hour.
   2. Parse all the JSON files and select the temperature values that occur within the quadrangle \[-125, 40, -120, 35 \] (upper left, lower right).
   3. Calculate the average temperature for that hour for that region.

### D. Parsing CSV: Grid Averages ###

#### Description ####

Comma Separated Values (CSV) is a very common but non-standardized data format.  The CWOP data set has been transformed into a simple set of CSV data files.  You should attempt to partition the data 
by quadrangles and produce a temperature summary for each quadrangle covering the continental USA (i.e., \[-125, 45, -65, 25\]).  A partitioning by 5° quadrangles will produce a 
12 by 4 grid over the region.

CSV data can be easily parsed in Python using the [csv module](https://docs.python.org/2/library/csv.html); see [csv-dump.py](csv-dump.py).

#### Tasks ####

    1. Pick a particular hour.
    2. Parse all the CSV files and select the subset within the region.  Assign report to grid cells.
    3. Calculate the average temperature for each grid cell.
   

### E. Direct Access to S3 via boto ###

#### Description ####

You can access S3 in python via the [boto module](http://boto.readthedocs.org/en/latest/s3_tut.html).  There are samples for outputting a key value ([s3cat.py](s3cat.py)), 
copying a file into s3 ([s3copy.py](s3copy.py)]), and list the keys in a bucket ([s3list.py](s3list.py)).

You need to set environment variables for the code to work as it needs your AWS key and secret:

    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...

The documentation is [available online](http://boto.readthedocs.org/en/latest/ref/s3.html).

#### Activity ####

You can repeat any of the activities above by accessing the data directly.

    1. Pick a previous activity for which you have working code.
    2. Modify the activity to read the list of files out of the bucket.
    3. Process the data directly by either temporarily storing the files locally or loading the contents into strings.
    
Note: You can list a subset of keys in a bucket by using the `prefix` parameter.  See [s3list.py](s3list.py) for an example.

  
  
