import unittest
import sys
sys.path.append("../src/twitter_bot")
from categorization_algorithm import *
from tiny_db_calls import *


class TestLanguageFunctions(unittest.TestCase):
    
    def test_word_filter(self):
        favorites = get_all_favorites('alittl3ton13',table="favorite_tbl")
        output = filter_out_words(favorites)
        self.assertTrue(type(output) == type({}))
        self.assertTrue(len(output.keys()) != 0)

if __name__ == "__main__":
    unittest.main()