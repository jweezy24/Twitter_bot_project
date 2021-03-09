import unittest
import sys
sys.path.append("../src/twitter_bot")
from categorization_algorithm import *
from tiny_db_calls import *

favorites = get_all_favorites('jack_west24',table="favorite_tbl")

class TestLanguageFunctions(unittest.TestCase):
    
    def test_word_filter(self):
        output = filter_out_words(favorites)
        self.assertTrue(type(output) == type({}))
        self.assertTrue(len(output.keys()) != 0)

    def test_rank_words_dictionary(self):
        output = filter_out_words(favorites)
        ranked = rank_words_dictionary(output)
        self.assertTrue(type(ranked) == type([]))
        self.assertTrue(len(ranked) != 0)

    def test_sentiment_calculation(self):
        t1 = "Fuck you. Fuck this."
        self.assertFalse(determine_sentiment_of_text(t1))
        t1 = "I love icecream!"
        self.assertTrue(determine_sentiment_of_text(t1))
        t1 = "Mormons live in Utah."
        self.assertTrue(determine_sentiment_of_text(t1))
        
        
if __name__ == "__main__":
    unittest.main()