import os
import twitter
import tweepy
import time
from word_examination import *
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
                save_value(entry._json,userid=user)
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
    for page in tweepy.Cursor(api2.favorites, screen_name=user).pages():
        for entry in page:
            if not search_value(entry._json["id"]):
                res = get_tweet_context(entry._json["id"])
                save_value(res,userid=user)
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

        results.append(tweet)
        if local_min == -1 or tweet._json['id'] < local_min:
            local_min = tweet._json['id']-1
    
    return retrieve_all_tweets(user,results,max_id=local_min)




''' 
    Returns a dictionary word list of all the user's most commonly assciated words.
    Data Structure used: List
    Input: A string of the user's screen name
    Output: a hashmap of commonly asscociated words
'''

def create_word_dictionary(user):
    words = {}
    results = []
    statuses = retrieve_all_statuses(user,results)
    favorites = get_favorites(user)

    for status in statuses:
        tweet = filter_out_words(status)

        for word in tweet:
            if word.lower() not in words:
                words[word.lower()] = 1
            else:
                words.update({word.lower(): words[word.lower()]+1})
    
    
    for favorite in favorites:
        tweet = favorite['text']
        tweet = filter_out_words(tweet)

        for word in tweet:
            if word.lower() not in words:
                words[word.lower()] = 1
            else:
                words.update({word.lower(): words[word.lower()]+1})

    return words
