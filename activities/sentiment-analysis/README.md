# Sentiment Analysis #

## Setup ##

Please make sure you have nltk installed:

    pip install nltk
    python -m nltk.downloader all

Things you might review:
    
  * A [short set of slides](http://courses.ischool.berkeley.edu/ds205/f14/sentiment-analysis.xhtml) (also found [here](sentiment-analysis.xhtml)) that will walk you through the [Candy Corn example](candy-corn.py).
  * A nice blog post on [using NLTK for sentiment analysis](http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/)
  * A short article on [Bag-of-words model on Wikipedia](http://en.wikipedia.org/wiki/Bag-of-words_model)
  
  
## Overview ##

We're going to work our way through training a classifier for to detect positive or negative sentiment.  This activity
will not make you an expert.  Instead, it is designed to give you a sense of the steps and data pipeline
necessary to run such a classifier.

We have a set of movie review data gathered from the "Rotten Tomatoes" website by Pang/Lee in 2005.  Each review has
been extracted from the page and turned into a single line of text that is categorized as positive or negative.

The data is found in the [rt-polaritydata](rt-polaritydata/) directory:

   * [rt-polarity.neg](rt-polarity.neg) — the original negative reviews in Windows 1252 text encoding
   * [rt-polarity.neg](rt-polarity.neg,utf8) — the negative reviews in UTF-8 text encoding
   * [rt-polarity.pos](rt-polarity.pos) — the original positive reviews in Windows 1252 text encoding
   * [rt-polarity.pos](rt-polarity.pos,utf8) — the positive reviews in UTF-8 text encoding
   
