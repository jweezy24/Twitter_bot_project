import unittest
import sys
sys.path.append("../src/twitter_bot")
from api_useage import *

''' THESE TESTS WILL REQUIRE PROPER ENVIRONMENT VARIABLES TO PROPERLY RUN.
    FOR QUESTIONS EMAIL JACK (jwest1@luc.edu) '''


class TestAPICalls(unittest.TestCase):
    
    ''' Verifies proper output of API calls '''

    def test_get_favorites(self):
        favs = get_favorites('alittl3ton13')
        self.assertFalse(favs == None)
        

    def test_get_followers(self):
        users = get_followers('jack_west24')
        self.assertTrue(len(users) == 61)

    def test_create_word_dictionary(self):
        words = create_word_dictionary('jack_west24')
        
        self.assertTrue(words == type({}))
        self.assertTrue(len(words) != 0)
    
    def test_retrieve_all_statuses(self):
        res = []
        tweets = retrieve_all_statuses('jack_west24',res)
        
        self.assertTrue(len(tweets) < 200)
        # self.assertTrue(words == type({}))
        # self.assertTrue(len(words) != 0)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    ''' DUE TO API LIMITATIONS RESERVE TESTING TO ONE METHOD AT A TIME '''
    #suite.addTest(TestAPICalls('test_get_favorites'))
    #suite.addTest(TestAPICalls('test_get_followers'))
    #suite.addTest(TestAPICalls('test_create_word_dictionary'))
    suite.addTest(TestAPICalls('test_retrieve_all_statuses'))

    unittest.TextTestRunner().run(suite)