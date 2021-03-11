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

    for page in tweepy.Cursor(api2.favorites, screen_name=user).pages():
        for entry in page:
            if not search_value(entry._json["id"]):
                save_value(entry._json,userid=user,table="favorite_tbl")
            else:
                continue
    
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

    for page in tweepy.Cursor(api2.favorites, screen_name=user).pages():
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


'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we are going to examine
Output: a list of tweets of that user.
'''

def retrieve_all_tweets(user,results,max_id=-1):
    
    if max_id == -1:
        tweets = api2.user_timeline(screen_name = user,count=200)
    else:
        tweets = api2.user_timeline(screen_name = user,count=200,max_id=max_id)
    
    local_min = -1  
    
    if len(tweets) == 0:
        return results

    ids = []
    count = 0
    for tweet in tweets:
        save_value(tweet._json,user,table="tweets")
        results.append(tweet)
        if local_min == -1 or tweet._json['id'] < local_min:
            local_min = tweet._json['id']-1
    
    return retrieve_all_tweets(user,results,max_id=local_min)

'''
The idea for this method came from here.
https://gist.github.com/yanofsky/5436496
Input: Username of user that we want to give context to.
'''

def save_all_tweets_context(user):

    tweets = get_all_table_entries(user, table="tweets")

    for entry in tweets:
        print(entry)
        res = get_tweet_context(entry["id"])
        if res:
            save_value(res,userid=user,table="tweets_context")
        else:
            continue


