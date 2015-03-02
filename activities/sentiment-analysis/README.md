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

We have a set of movie review data gathered from the ["Rotten Tomatoes" website by Pang/Lee in 2005](http://www.cs.cornell.edu/People/pabo/movie-review-data/).  Each review has
been extracted from the page and turned into a single line of text that is categorized as positive or negative.

The data is found in the [rt-polaritydata](rt-polaritydata/) directory:

   * [rt-polarity.neg](rt-polarity.neg) — the original negative reviews in Windows 1252 text encoding
   * [rt-polarity.neg.utf8](rt-polarity.neg.utf8) — the negative reviews in UTF-8 text encoding
   * [rt-polarity.pos](rt-polarity.pos) — the original positive reviews in Windows 1252 text encoding
   * [rt-polarity.pos.utf8](rt-polarity.pos.utf8) — the positive reviews in UTF-8 text encoding
   
To apply the bag-of-words model, we must:

  1. Decide on a set of "feature words" for the model.  These might be words like "bad", "good", "excellent", "horrible".
  2. Process our data to produce a feature vector for each review text.
  3. Train a classifier (e.g. a [Naive Bayse classifier](http://en.wikipedia.org/wiki/Naive_Bayes_classifier) on the data.
  4. Apply the classifier non-annotated data (i.e. new reviews).
  
There are two simple examples of this process:

   * [candy-corn.py](candy-corn.py) — an example of positive/negative sentiment (2-way classifier)
   * [n-way.py](n-way.py) — an example of a multiple category (>2) classifier
   
   
