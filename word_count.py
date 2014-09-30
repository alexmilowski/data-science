from collections import Counter
###
from mrcc import CCJob


class WordCount(CCJob):
  def process_record(self, record):
    if record['Content-Type'] != 'text/plain':
      return
    data = record.payload.read()
    #for word in data.split():
    #  yield word, 1
    for word, count in Counter(data.split()).iteritems():
      yield word, 1
    self.increment_counter('commoncrawl', 'processed_pages', 1)

if __name__ == '__main__':
  WordCount.run()
