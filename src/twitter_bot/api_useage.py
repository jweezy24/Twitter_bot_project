import os
import twitter
import tweepy
import time
from categorization_algorithm import *
from REST_api_calls import *
from tiny_db_calls import *


api_key = os.environ['APIKEY']
api_secret = os.environ['APISECRET'] 
username = os.environ['TWITTERUSER']
password = os.environ['TWITTERPASS']

print(api_key)

api = twitter.Api(consumer_key=username,
                consumer_secret=password,
                access_token_key=api_key,
                access_token_secret=api_secret)

auth = tweepy.OAuthHandler(username, password) 
  
# set access to user's access key and access secret  
auth.set_access_token(api_key, api_secret)
api2 = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

''' Returns a list of favorites in a Json format '''

def get_favorites(user,total=100):
    favs = []
    count = 0
    max_id = get_maximum_id(user, "favorite_tbl")
    for page in tweepy.Cursor(api2.favorites, screen_name=user, since_id=max_id).pages():
        for entry in page:
            if not search_value(entry._json["id"],user,table="favorite_tbl"):
                save_value(entry._json,userid=user,table="favorite_tbl")
                count+=1
                print("ADDED FAVORITE")
            else:
                continue
    print(f"ADDED {count} NEW FAVORITES")
    return favs


''' 
    Returns a list of favorites in a Json format.
    This method focuses on favoirites with context.
    input:
        user = screen name of the user you would like to get their favorites from
        total (optional) = the total number of favorites you would like to retrieve. default=100
    output:
        a list of favorites that are specficially contextual. 
'''

def get_favorites_with_context(user,total=100):
    favs = []
    count = 0
    table_cache = {"favorite_with_context_tbl" : None}
    max_id = get_maximum_id(user, "favorites_context")

    for page in tweepy.Cursor(api2.favorites, screen_name=user,since_id =max_id).pages():
        for entry in page:
            if not search_value(entry._json["id"], user, table="favorites_context"):
                res = get_tweet_context(entry._json["id"])
                if res:
                    tmp_id = entry._json["id"]
                    print(f"Saved {tmp_id}")
                    save_value(res,userid=user,table="favorites_context")
            else:
                continue
            if res:
                favs.append(res)
                
        
    

    return favs



''' 
    Returns a list of followers
    Data Structure used: List
    Input: A string of the user's screen name
    Output: A list of strings with each followers' screen_name
'''

def get_followers(user):
    names = []
    count = 0
    twitter_followers = get_followers_REST(user)
    current_followers = get_all_table_entries(user,"followers")
    print(f"Table size = {len(current_followers)} Twitter record = {len(twitter_followers)}" )
    if len(current_followers) != len(twitter_followers):
        for follower in current_followers:
            name = follower["id"]
            if name not in twitter_followers:
                print(f"Removed {name}")
                remove_from_table(user,"followers",name)

    
        for entry in twitter_followers:
            cached_entry = {"id":entry}
            if not search_value(cached_entry["id"], user, table="followers"):
                print(f"Saved Followers {entry}")
                save_value(cached_entry,userid=user,table="followers")

def get_following(user):
    names = []
    count = 0
    twitter_followers = get_following_REST(user)
    current_followers = get_all_table_entries(user,"following")
    print(f"Table size = {len(current_followers)} Twitter record = {len(twitter_followers)}" )
    if len(current_followers) != len(twitter_followers):
        for follower in current_followers:
            name = follower["id"]
            if name not in twitter_followers:
                print(f"Removed {name}")
                remove_from_table(user,"following",name)

    
        for entry in twitter_followers:
            cached_entry = {"id":entry}
            if not search_value(cached_entry["id"], user, table="following"):
                print(f"Saved Following {entry}")
                save_value(cached_entry,userid=user,table="following")


'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we are going to examine
Output: a list of tweets of that user.
'''

def retrieve_all_tweets(user,max_id=-1):
    
    data = api2.get_user(user)
    created = data.created_at
    favs = []
    count = 0
    max_id = get_maximum_id(user, "tweets")
    print(max_id)
    if max_id == None:
        cur = tweepy.Cursor(api2.user_timeline, id=user, since=created ).pages()
    else:
        cur = tweepy.Cursor(api2.user_timeline, id=user,since_id =max_id).pages()
    
    count = 0
    for page in cur:
        for entry in page:
            if not search_value(entry._json["id"], user, table="tweets"):
                    print(f"Saved Tweet")
                    save_value(entry._json,userid=user,table="tweets")
                    count+=1

    print(f"Saved {count} Tweets from {user}")    
'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we want to give context to.
'''

def save_all_tweets_context(user,max_id=-1):

    data = api2.get_user(user)
    created = data.created_at
    favs = []
    count = 0
    max_id = get_maximum_id(user, "tweets_context")
    print(max_id)
    if max_id == None:
        cur = tweepy.Cursor(api2.user_timeline, id=user, since=created ).pages()
    else:
        cur = tweepy.Cursor(api2.user_timeline, id=user,since_id =max_id).pages()
    
    for page in cur:
        for entry in page:
            if not search_value(entry._json["id"], user, table="tweets_context"):
                    save_value(entry._json,userid=user,table="tweets_context")


def build_user_web(user):
    print(f"Creating user web for {user}")
    followers = get_all_table_entries("followers")
    following = get_all_table_entries("following")

    if not followers:
        get_followers(user)
        followers = get_all_table_entries(user,"followers")
    if not following:
        get_following(user)
        following = get_all_table_entries(user,"following")

    print(f"{user} is Following {following}")
    print(f"{user} is Followed by {followers}")

    for people in followers:
        people = people["id"]
        print(f"CHECKING {people}")
        retrieve_all_tweets(people)
        print(f"Got Tweets for {people}")
        save_all_tweets_context(people)
        print(f"Got Tweets with context for {people}")
        get_favorites(people)
        print(f"Got favorites for {people}")
        get_favorites_with_context(people)
        print(f"Got favorites with context for {people}")
        

    for people in followers:
        people = people["id"]
        print(f"CHECKING {people}")
        retrieve_all_tweets(people)
        print(f"Got Tweets for {people}")
        save_all_tweets_context(people)
        print(f"Got Tweets with context for {people}")
        get_favorites(people)
        print(f"Got favorites for {people}")
        get_favorites_with_context(people)
        print(f"Got favorites with context for {people}")

        

if __name__ == "__main__":
    #Below average twitter account in size
    build_user_web('jack_west24')
    #Normal twitter account with consistant activity
    build_user_web('alittl3ton13')
    #Very little activity and size
    build_user_web('allyssa_fogarty')
    #Large activity and size
    build_user_web('theneedledrop')
