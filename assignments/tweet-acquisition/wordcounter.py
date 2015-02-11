import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, tweet):
        for term in get_terms(tweet['text']):
            yield term, 1

    def reducer(self, term, occurrences):
        yield None, {term: sum(occurrences)}

if __name__ == '__main__':
        MRWordCount.run()
