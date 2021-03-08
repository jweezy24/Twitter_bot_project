import unittest
import sys
sys.path.append("../src/twitter_bot")
from categorization_algorithm import *


class TestLanguageFunctions(unittest.TestCase):
    
    def test_word_filter(self):
        text = "Being more Pythonic is good for the health."
        words = filter_out_words(text)
        correct_words = ['Being', 'more', 'Pythonic', 'good', 'health']
        self.assertTrue(correct_words == words)



if __name__ == "__main__":
    unittest.main()