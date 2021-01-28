import unittest
import sys
sys.path.append("../src/twitter_bot")
from api_useage import *

''' THESE TESTS WILL REQUIRE PROPER ENVIRONMENT VARIABLES TO PROPERLY RUN.
    FOR QUESTIONS EMAIL JACK (jwest1@luc.edu) '''


class TestAPICalls(unittest.TestCase):
    
    ''' Verifies proper output of API calls '''

    def test_get_favorites(self):
        favs = get_favorites('jack_west24')
        self.assertFalse(favs == None)
    
    def test_get_followers(self):
        users = get_followers('jack_west24')
        print(users)



if __name__ == "__main__":
    unittest.main()