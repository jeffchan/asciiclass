import twitter_pb2
import sys

class TweetAnalysis:
	def __init__(self, tweets):
		self.tweets = tweets

	def total(self):
		return len(self.tweets)

	def numDeleted(self):
		return len([tweet for tweet in self.tweets if tweet.is_delete])

	def tweetIds(self):
		return [tweet.insert.id for tweet in self.tweets]

	def numReplies(self):
		ids = self.tweetIds()
		return len([tweet for tweet in self.tweets if tweet.insert.HasField('reply_to') and ids.count(tweet.insert.reply_to) >= 1])

	def topUids(self):
		count = dict()
		for tweet in self.tweets:
			uid = str(tweet.insert.uid)
			if uid in count:
				count[uid] = (count[uid][0]+1, uid)
			else:
				count[uid] = (1, uid)
		return sorted(count.values(), key=lambda x: x[0], reverse=True)[:5]

	def topPlaces(self):
		count = dict()
		for tweet in self.tweets:
			if tweet.insert.HasField('place'):
				place = tweet.insert.place
				id = str(place.id)
				if id in count:
					count[id] = (count[id][0]+1, place.name)
				else:
					count[id] = (1, place.name)
		return sorted(count.values(), key=lambda x: x[0], reverse=True)[:5]

if len(sys.argv) != 2:
	print 'Usage:', sys.argv[0], '<file>'
	sys.exit(-1)

twitter = twitter_pb2.Tweets()
f = open(sys.argv[1], 'rb')
twitter.ParseFromString(f.read())
f.close()

analysis = TweetAnalysis(twitter.tweets)

print 'Total tweets:', analysis.total()
print 'Number of deleted tweets:', analysis.numDeleted()
print 'Number of replies to another tweet in this dataset:', analysis.numReplies()
print 'Top 5 uids:', analysis.topUids()
print 'Top 5 places:', analysis.topPlaces()
