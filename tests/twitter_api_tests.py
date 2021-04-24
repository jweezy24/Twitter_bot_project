import unittest
import sys
sys.path.append("../src/twitter_bot")
from api_useage import *
from REST_api_calls import *
from user_obj import *

''' THESE TESTS WILL REQUIRE PROPER ENVIRONMENT VARIABLES TO PROPERLY RUN.
    FOR QUESTIONS EMAIL JACK (jwest1@luc.edu) '''


class TestAPICalls(unittest.TestCase):
    
    ''' Verifies proper output of API calls '''

    def test_get_favorites(self):
        favs = get_favorites('jack_west24')
        self.assertFalse(favs == None)
        print(favs)
    
    def test_get_favorites_context(self):
        favs = get_favorites_with_context('jack_west24')
        self.assertFalse(favs == None)
        print(favs)
        
    def test_get_followers(self):
        users = get_followers('jack_west24')
        
    
    def test_get_following(self):
        users = get_following('jack_west24')
        
    
    def test_retrieve_all_tweets(self):
        retrieve_all_tweets('jack_west24')
        tweets = get_all_table_entries("jack_west24","tweets")

        self.assertTrue(len(tweets) >=  1)
        # self.assertTrue(words == type({}))
        # self.assertTrue(len(words) != 0)

    def test_get_context(self):
        tweet_id = 1361392458383384578
        print(get_tweet_context(tweet_id))

    def test_twitter_acc(self):
        user = twitter_account('alittl3ton13')
        
        print(user.get_favorites())
        print(user.get_followers())
        print(user.get_tweets())

        self.assertTrue(user.get_favorites() != None)
        self.assertTrue(user.get_followers() != None)
        self.assertTrue(user.get_tweets() != None)

    def test_save_all_tweets_context(self):
        save_all_tweets_context('jack_west24')

    def test_get_followers_REST(self):
        get_followers_REST('jack_west24')

    def test_get_rate_limit(self):
        print(get_rate_limit())

if __name__ == "__main__":
    suite = unittest.TestSuite()
    ''' DUE TO API LIMITATIONS RESERVE TESTING TO ONE METHOD AT A TIME '''
    #suite.addTest(TestAPICalls('test_get_favorites'))
    #suite.addTest(TestAPICalls('test_get_favorites_context'))
    #suite.addTest(TestAPICalls('test_get_followers'))
    #suite.addTest(TestAPICalls('test_get_following'))
    #suite.addTest(TestAPICalls('test_create_word_dictionary'))
    #suite.addTest(TestAPICalls('test_retrieve_all_tweets'))
    #suite.addTest(TestAPICalls('test_get_context'))
    #suite.addTest(TestAPICalls('test_twitter_acc'))
    #suite.addTest(TestAPICalls('test_save_all_tweets_context'))
    suite.addTest(TestAPICalls('test_get_rate_limit'))
    #suite.addTest(TestAPICalls('test_get_followers_REST'))
    
    unittest.TextTestRunner().run(suite)