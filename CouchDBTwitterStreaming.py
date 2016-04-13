
# to l0ok for tweets storage in database http://127.0.0.1:5984/test_db/_design/twitter/_view/get_tweets
# this module is about how to store and retrieve tweets from couchdb database also include functionality of MapReduce

import couchdb
import couchdb.design
from TwitterAPI.TwitterAPI import TwitterAPI

# To install above libraries use these following commands
# First download appropriate sofware http://couchdb.apache.org/#download for your OS
# Use [Anaconda3] C:\Users\User>pip install -i https://pypi.anaconda.org/pypi/simple couchdb for python couchdb support
# Use [Anaconda3] C:\Users\User>pip install TwitterAPI  to install Twitter API library   
COUCH_SERVER = 'http://127.0.0.1:5984/'


class TweetStore(object):
    def __init__(self, dbname, url=COUCH_SERVER):
        try:
            #url used for accessing couchDB server
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
            self._create_views()
        except couchdb.http.PreconditionFailed:
            # if db already exist then catch error and store in it
            self.db = self.server[dbname]
#counting nuber of tweets in database
    def _create_views(self):
        count_map = 'function(doc) { emit(doc.id, 1); }'
        count_reduce = 'function(keys, values) { return sum(values); }'
        view = couchdb.design.ViewDefinition('twitter', 'count_tweets', count_map, reduce_fun=count_reduce)
        view.sync(self.db)

        #printing all of tweets in database, We adding zeroes to str to maintian chronological order and same length key
        get_tweets = 'function(doc) { emit(("0000000000000000000"+doc.id).slice(-19), doc); }'
        view = couchdb.design.ViewDefinition('twitter', 'get_tweets', get_tweets)
        view.sync(self.db)

    def save_tweet(self, tw):
        #storing tweets in database as couchdb as similar format to json so required doc and id field rmain same and using tweet id
    # for database index
        tw['_id'] = tw['id_str']
        self.db.save(tw)

    def count_tweets(self):
        for doc in self.db.view('twitter/count_tweets'):
            return doc.value

    def get_tweets(self):
        return self.db.view('twitter/get_tweets')
print ("completed")

# This module is about how to connect to TwitterApi with credentials and retrieve tweets from Twitter specifying particular keyword
#and using stramline method of twitter to get live tweets till we break the connection as in TCP.

COUCH_DATABASE = 'test_db'
TWITTER_ENDPOINT = 'statuses/filter'
TWITTER_PARAMS = {'track':'AFL'}

API_KEY = '2wiCvpRgCUIXqsBSUVuiz7ah7'
API_SECRET = 'JNPFoGr8GBnok6m7Kc3X4UiqEJ5F6eWoVNwbDOtAM4YEGOVdwV'
ACCESS_TOKEN = '4033248678-FAmGUL2ewNozSV6xHIG3ffgeS5cKkQIBuk8PgaV'
ACCESS_TOKEN_SECRET = 'XIILB8Ueds2Xc7FAZ1TskFCLPc0Uc2VDQemeyrFcWL4U5'

storage = TweetStore(COUCH_DATABASE)

#t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_SECRET, API_KEY))
#x = t.application.rate_limit_status()
#print(x['resources']['users']) 
#print ("completed")

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


for item in api.request(TWITTER_ENDPOINT, TWITTER_PARAMS):
    if 'text' in item:
        #print('%s -- %s\n' % (item['user']['screen_name'], item['text']))
        storage.save_tweet(item)
    elif 'message' in item:
        print('ERROR %s: %s\n' % (item['code'], item['message']))
print ("completed")

# Module halp to build a real couchdb database and store tweetcount and tweet text to it

COUCH_DATABASE = 'test_db'


storage = TweetStore(COUCH_DATABASE)

print('tweet count is %d\n' % storage.count_tweets())

for doc in storage.get_tweets():
    print('%s\n' % doc.value['text'])
print ("completed")