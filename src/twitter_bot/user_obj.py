from api_useage import *

class twitter_account:
    def __init__(self, screen_name):
        self.favorites = get_favorites(screen_name)
        self.followers = get_followers(screen_name)
        self.tweets = []
        retrieve_all_tweets(screen_name,self.tweets)

    def get_favorites(self):
        return self.favorites
    
    def get_followers(self):
        return self.follwers
    
    def get_tweets(self):
        return self.tweets