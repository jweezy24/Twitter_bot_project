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
        users = create_word_dictionary('jack_west24')



if __name__ == "__main__":
    suite = unittest.TestSuite()
    ''' DUE TO API LIMITATIONS RESERVE TESTING TO ONE METHOD AT A TIME '''
    #suite.addTest(TestAPICalls('test_get_favorites'))
    #suite.addTest(TestAPICalls('test_get_followers'))
    suite.addTest(TestAPICalls('test_create_word_dictionary'))

    unittest.TextTestRunner().run(suite)