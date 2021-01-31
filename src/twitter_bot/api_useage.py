import os
import twitter
import tweepy
import time


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
api2 = tweepy.API(auth) 

''' Returns a list of favorites in a Json format '''

def get_favorites(user):
    favs = api.GetFavorites(screen_name=user, return_json=True,count=200)
    return favs


''' 
    Returns a list of followers
    Data Structure used: List
    Input: A string of the user's screen name
    Output: A list of strings with each followers' screen_name
'''

def get_followers(user):
    names = []
    for page in tweepy.Cursor(api2.followers, screen_name=user).pages():
        for entry in page:
            names.append(entry._json['screen_name'])
        
        time.sleep(10)
    
    return names


''' 
    Returns a dictionary word list of all the user's most commonly assciated words.
    Data Structure used: List
    Input: A string of the user's screen name
    Output: a hashmap of commonly asscociated words
'''

def create_word_dictionary(user):
    words = {}
    statuses = api2.user_timeline(user,count=200)
    favorites = get_favorites(user)

    for status in statuses:
        tweet = status._json['text']

        for word in tweet.split():
            if word.lower() not in words:
                words[word.lower()] = 1
            else:
                words.update({word.lower(): words[word.lower()]+1})
    
    
    for favorite in favorites:
        tweet = favorite['text']

        for word in tweet.split():
            if word.lower() not in words:
                words[word.lower()] = 1
            else:
                words.update({word: words[word.lower()]+1})

    return words