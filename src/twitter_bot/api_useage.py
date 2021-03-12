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

    for page in tweepy.Cursor(api2.favorites, screen_name=user,max_id =max_id).pages():
        for entry in page:
            if not search_value(entry._json["id"], user, table="favorites_context"):
                res = get_tweet_context(entry._json["id"])
                if res:
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

def get_followers(user, total=100):
    names = []
    count = 0
    for page in tweepy.Cursor(api2.followers, screen_name=user).pages():
        for entry in page:
            if count < total:
                names.append(entry._json['screen_name'])
                count+=1
            else:
                break
        
        if count >= total:
            break
    
    return names

def get_following(user, total=100):
    names = []
    count = 0
    for page in tweepy.Cursor(api2.friends, screen_name=user).pages():
        for entry in page:
            if count < total:
                names.append(entry._json['screen_name'])
                count+=1
            else:
                break
        
        if count >= total:
            break
    
    return names


'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we are going to examine
Output: a list of tweets of that user.
'''

def retrieve_all_tweets(user,max_id=-1):
    
    
    favs = []
    count = 0
    max_id = get_maximum_id(user, "tweets")
    print(max_id)
    if max_id == None:
        cur = tweepy.Cursor(api2.user_timeline, id=user).pages()
    else:
        cur = tweepy.Cursor(api2.user_timeline, id=user,since_id =max_id).pages()
    
    for page in cur:
        for entry in page:
            if not search_value(entry._json["id"], user, table="tweets"):
                    save_value(entry._json,userid=user,table="tweets")
    
'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we want to give context to.
'''

def save_all_tweets_context(user,max_id=-1):

    tfavs = []
    count = 0
    max_id = get_maximum_id(user, "tweets_context")
    print(max_id)
    if max_id == None:
        cur = tweepy.Cursor(api2.user_timeline, id=user).pages()
    else:
        cur = tweepy.Cursor(api2.user_timeline, id=user,since_id =max_id).pages()
    
    for page in cur:
        for entry in page:
            if not search_value(entry._json["id"], user, table="tweets_context"):
                    save_value(entry._json,userid=user,table="tweets_context")


def build_user_web(user):
    followers = get_followers(user)
    following = get_following(user)

    for people in followers:
        retrieve_all_tweets(people)
        save_all_tweets_context(people)
        get_favorites(people)
        get_favorites_with_context(people)
        

    for people in followers:
        retrieve_all_tweets(people)
        save_all_tweets_context(people)
        get_favorites(people)
        get_favorites_with_context(people)
        
