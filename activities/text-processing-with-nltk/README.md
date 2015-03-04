# Text Processing with NLTK #

## Setup ##

NLTK is a module for python for processing "natural languages".  It also contains supporting data files 
(e.g., stop word lists by langauge) necessary for some of the algorithms to function. 

To install NLTK for yourself, do the following:

    pip install nltk
    python -m nltk.downloader all
    
If you are on a Max OS X / Linux system, you may want to install the NLTK module for everyone:

    sudo pip install nltk
    sudo python -m nltk.downloader -d /usr/share/nltk_data all
    
To test that you've got everything installed:

    from nltk.book import *
    text1.concordance("whale")
    
should print a list of phrases in Moby Dick that contain the word 'whale'.

## Basics of Tokenization ##

Many algorithms for processing text require taking passages of text and turn them into sentences and words.  The process of doing is very 
specific to the language being processed and possibily influenced by how the text was collected or the genre of communication.

In general, langauges like English, Spanish, and other modern european languages are directly supported by the corpus of configuration data
provided by NLTK.  These languages also share common mechanism for simple tokenization into sentences and words.

A passage of text, like the above, can be first be broken down into sentences and then into words:
```
   import nltk
   
   text = '''Many algorithms for processing text require taking passages of text and turn them into sentences
   and words.  The process of doing is very specific to the language being processed and possibily influenced 
   by how the text was collected or the genre of communication.'''
   
   sentences = nltk.tokenize.sent_tokenize(text)
   
   for s in sentences:
      words = nltk.tokenize.word_tokenize(s)
      print words
```      
Notice how the punctuation of the sentences are mixed in with the words.  Tokenization doesn't take into account any
syntax that might be present.  As such, text tha contains any kind of annotation, URLs, etc. may need to be filtered
when turned into word tokens.

Futher, words can be annotated independently for their "parts of speech" (POS):

    import nltk
   
    s = "The quick brown fox jumped over the fence."
    words = nltk.tokenize.word_tokenize(s)
    nltk.pos_tag(words)
    
which should produce:

    [('The', 'DT'), ('quick', 'NN'), ('brown', 'NN'), ('fox', 'NN'), ('jumped', 'VBD'), ('over', 'IN'), ('the', 'DT'), ('fence', 'NN'), ('.', '.')]
    
Each of the codes can be looked up in the help:

    >>> nltk.help.upenn_tagset('DT')
    DT: determiner
        all an another any both del each either every half la many much nary
        neither no some such that the them these this those
    >>> nltk.help.upenn_tagset('NN')
    NN: noun, common, singular or mass
        common-carrier cabbage knuckle-duster Casino afghan shed thermostat
        investment slide humour falloff slick wind hyena override subhumanity
        machinist ...

## Stopwords ##

Many languages contain words that occur very often (e.g., "the" or "a" in English) and their frequent use will
overwhelm more interesting words useful in analysis.  A common technique is to use a stop word list to exclude
such common words from further processing.

NLTK supports stop words for a number of languages and they are accessed as:

    stopWords = nltk.corpus.stopwords.words('english')
    >>> stopWords
    [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', 
     u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', 
     u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', 
     u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', 
     u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', 
     u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', 
     u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', 
     u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', 
     u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', 
     u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', 
     u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', 
     u'don', u'should', u'now']
     
The `nltk.corpus.stopwords` module just returns a simple list of words you can use in your own code.  For example,
a simple list comprehension can be used to filter a list of words:

    stopWords = nltk.corpus.stopwords.words('english')
    filtered = [e.lower() for e in words if not e.lower() in stopWords]
    
and another trick is to add your list of punctuation to the stop word list:

    stopWords = nltk.corpus.stopwords.words('english') + ['.',',']
    filtered = [e.lower() for e in words if not e.lower() in stopWords]

The languages supported by NLTK can be discovered by inspecting the `nltk.corpus.stopwords` object:

    >>> nltk.corpus.stopwords
    <WordListCorpusReader in u'/usr/share/nltk_data/corpora/stopwords'>

The reader outputs the directory in which the stop words are stored.  You can list the suppored langauges:

    $ ls /usr/share/nltk_data/corpora/stopwords
    README		english		german		norwegian	spanish
    danish		finnish		hungarian	portuguese	swedish
    dutch		french		italian		russian		turkish
    $ head -n 10 /usr/share/nltk_data/corpora/stopwords/english
    i
    me
    my
    myself
    we
    our
    ours
    ourselves
    you
    your 

The files contain a single word per line.  As such, you can create or modify a stop word list for any language and add it to NLTK.

## Frequency Distributions ##

A frequency distribution can be constructed from the a list as a construction parameter:

    import nltk
    words = [ 'A', 'A', 'B', 'B', 'B', 'C']
    fd = FreqDist(words)
    fd.tabulate()
    
produces the output:

       B    A    C 
       3    2    1 
       
You can also produce a visual plot by calling `plot()`.

A frequency distribution can be constructed iteratively as well:

    fd = FreqDist()
    for w in words:
       fd[w.lower()] += 1
    
or via a comprehension:

    fd = FreqDist(w.lower() for w in words)

## Stemming and Lemminization #

Stemming: the process for reducing inflected (or sometimes derived) words to their stem, base or root form.

Lemmatization: the process of grouping together the different inflected forms of a word so they can be analysed as a single item.

NLTK supports:

  * [Porter Stemming](http://tartarus.org/martin/PorterStemmer/)
  * [Lancaster Stemming](http://www.comp.lancs.ac.uk/computing/research/stemming/)
  * [Snowball Stemming](http://snowball.tartarus.org)
  * Lemminization based on [WordNet’s built-in morphy function](http://wordnet.princeton.edu)

For stemming, you construct a stemmer and then call `stem()` on the word:

    from nltk.stem.lancaster import LancasterStemmer
    stemmer = LancasterStemmer()
    w = lancaster_stemmer.stem(‘presumably’)  # returns u’presum’

In the above, you can use `nltk.stem.porter.PorterStemmer`, `nltk.stem.lancaster.LancasterStemmer`, or `nltk.stem.SnowballStemmer`.

Lemmatization is similar:

    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatizer.lemmatize(‘dogs’)  # returns u'dog'
    
but the lemmatizer assumes by default everything is a noun.  For verbs, this means that results are not lemmatized 
properly (e.g., "are" and "is" do not become "be").

For example, try:

    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    lemmatizer.lemmatize('is',pos='v')
    lemmatizer.lemmatize('are',pos='v')
    
The `pos` argument can have the following values:

   * 'a' - adjective
   * 'r' - adverb
   * 'n' - noun
   * 'v' - verb

## Activity ##

Pick a passage of text and:

   1. Tokenize the text.
   2. List all the nouns in the passage.
   3. Apply a stop word filter to the tokenized text.
   4. Compute and plot a frequency distribution of the top 50 words.
   5. Apply a lemmatization algorithm with the pos argument set to 'n' and recompute your frequency distribution.
   
