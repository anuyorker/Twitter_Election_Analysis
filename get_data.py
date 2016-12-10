import tweepy
import json
import time
import sys
import cred

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, api=None, prefix='stream'):
		self.prefix = prefix
		self.api = api
		self.output = '%s_%s.json' % (prefix, time.strftime('%Y%m%d-%H%M%S'))

	def on_data(self, data):
		while True:
			try:
				with open(self.output, 'a', encoding='utf-8') as f:
					parsedjson = json.loads(data)
					prettydata = json.dumps(parsedjson, sort_keys=True, indent=4)
					f.write(prettydata)
					print(data[:75])

					#print(prettydata)
					time.sleep(2) # to prevent rate limits
				return True

			except BaseException as e:
				print('Error with retrieve_data(): %s' % str(e))
				time.sleep(5)
				continue

	def on_status(self, status):
		print(status.text.encode('utf-8'))

	def on_error(self, status_code):
		if status_code == 420:
			print('Caught 420 (rate limit) error! Returning False and stopping.')
			#returning False in on_data disconnects the stream
			return False
		else:
			print('Got an error w/ status code: ' + str(status_code))
			return True


if __name__ == '__main__':

	
	while True:
		try:
			myStreamListener = MyStreamListener()
			auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
			auth.set_access_token(cred.access_token, cred.access_token_secret)
			api = tweepy.API(auth)

			myStream = tweepy.Stream(auth, myStreamListener)
			myStream.filter(track=['election', 'donald', 'trump', 'hillary', 'clinton', 'debates', \
								   '#election2016', '#electionday', '#ivoted', '#imwithher', '#makeamericagreatagain' \
								   'vote', '#2016election', 'politics', '#lockherup', '#deleteyouraccount', '#crookedhillary' \
								   '#nevertrump', '#feelthebern', '#blacklivesmatter', '#imvotingbecause', 'equality', \
								   '#thirdparty', '#garyjohnson', 'ballot', 'obama', '#electionfinalthoughts'])			
		except: 
			continue

