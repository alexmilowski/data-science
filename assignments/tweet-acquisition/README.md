Bucket Location:
https://moonlightbucket.s3.amazonaws.com/
How to retrieve tweets with the keywords and store on S3
1.	Command format: python “startdate” “enddate”
2.	In the beginning, I had one script to get tweets for the entire week. However, my Linux VM had numerous issues, including 1)KILLED message showing up 2)running out of disc space. Thus, I turned “start” and “end” date into command line arguments so I can query a day’s worth of tweets each time. This way, if retrieval failed, I only have to rerun the retrieval for the specified day. The downside of this is that I had to run the command manually 7 times:
 python “2015-02-07” “2015-02-08”
python “2015-02-08” “2015-02-09”
python “2015-02-09” “2015-02-10”
python “2015-02-10” “2015-02-11”
python “2015-02-11” “2015-02-12”
python “2015-02-12” “2015-02-13”
python “2015-02-13” “2015-02-14”

How to analyze tweets on S3 and create histogram. 
1.	Run “python analyze.py”
2.	First I tried to create histogram from entire data. However, my VM kept giving me a “KILLED” error(http://stackoverflow.com/questions/19189522/what-does-killed-mean-in-python).
Therefore, I decided to make a histogram only for words with more 1000 counts. Please see “histogramForOver1000Counts.png”.




  
