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

    def test_combine_favorites_with_context(self):
        #final = combine_favorites_with_context('alittl3ton13')
        final2 = combine_tweets_with_context('alittl3ton13')
        #output1,output2,output3 = filter_out_words(final)
        output4,output5,output6 = filter_out_words(final2)
        #ranked = rank_words_dictionary(output1)
        ranked4 = rank_words_dictionary(output4)
        #ranked2,ranked2_neg = rank_context_dictionary(output2)
        #ranked3,ranked3_neg = rank_context_dictionary(output3)
        # pretty_print_context(ranked2)
        # pretty_print_context(ranked2_neg)
        # pretty_print_context(ranked3)
        # pretty_print_context(ranked3_neg)
        # pretty_print(ranked4)
        # self.assertTrue(type(ranked) == type([]))
        # self.assertTrue(len(ranked) != 0)

        
if __name__ == "__main__":
    #unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(TestLanguageFunctions("test_combine_favorites_with_context"))
    runner = unittest.TextTestRunner()
    runner.run(suite)