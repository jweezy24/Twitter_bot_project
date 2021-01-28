import os
import twitter
import tweepy
import time


api_key = os.environ['APIKEY']
api_secret = os.environ['APISECRET'] 
bearer_token = os.environ['BEARER']
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
api2 = tweepy.API(auth) 

''' Returns a list of favorites in a Json format '''

def get_favorites(user):
    favs = api.GetFavorites(screen_name=user, return_json=True)
    return favs


''' 
    Returns a list of followers
    Data Structure used: List
    Input: A string of the user's screen name
    Output: A list of strings with each followers' screen_name
'''

def get_followers(user):
    users = api2.friends(user)
    names = []
    for i in users:
        print(i)
        #names.append(user["screen_name"])
    

    return names