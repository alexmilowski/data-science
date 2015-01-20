import json

class TweetSerializer:
	out = None
	first = True

	file_count = 0
	current_file_tweet_count = 0
	max_tweet_count_per_file = 0

	def __init__(self, max_tweet_count_per_file):
		self.current_file_tweet_count = 0
		self.max_tweet_count_per_file = max_tweet_count_per_file

	def open_file(self):
		self.file_count += 1
		fname = "tweets-" + str(self.file_count) + ".json"
		self.out = open(fname,"w")
		self.out.write("[\n")
		self.first = True

	def close_file(self):
		if self.out is not None:
			self.out.write("\n]\n")
			self.out.close()

		self.out = None
		self.current_file_tweet_count = 0

	def write(self,tweet):
		if self.out is None:
			self.open_file()

		if not self.first:
			self.out.write(",\n")

		self.first = False
		self.out.write(json.dumps(tweet._json).encode('utf8'))

		self.current_file_tweet_count += 1

		if self.current_file_tweet_count == self.max_tweet_count_per_file:
			self.close_file()
