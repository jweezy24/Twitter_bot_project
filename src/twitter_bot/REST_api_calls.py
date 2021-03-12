import requests
import os
import json
bear = os.environ["BEARER"]

def get_tweet_context(ids):
    string = ''

    '''
    If the variable ids is a list we create a string of comma separated ids.
    '''
    if type(ids) == type([]):
        for id in ids:
            string += f"{id},"
        string=string[:len(string)-2]
        
        r = requests.get(f'https://api.twitter.com/2/tweets?ids={string}&tweet.fields=context_annotations', headers={'Authorization' : f'Bearer {bear}'})
        
    elif type(ids) == type("") or type(ids) == type(1):
        r = requests.get(f'https://api.twitter.com/2/tweets/{ids}?&tweet.fields=context_annotations', headers={'Authorization' : f'Bearer {bear}'})

    else:
        r = None


    if r and "context_annotations" in r.json()["data"]:
        return r.json()["data"]
    else:
        return None

def get_followers_REST(user):
    r1 = requests.get(f'https://api.twitter.com/2/users/by/username/{user}', headers={'Authorization' : f'Bearer {bear}'})

    id = r1.json()["data"]["id"]
    r1 = requests.get(f'https://api.twitter.com/2/users/{id}/followers?&user.fields=name', headers={'Authorization' : f'Bearer {bear}'})

    
    return r1.json()["data"]

def get_following_REST(user):
    r1 = requests.get(f'https://api.twitter.com/2/users/by/username/{user}', headers={'Authorization' : f'Bearer {bear}'})

    id = r1.json()["data"]["id"]
    r1 = requests.get(f'https://api.twitter.com/2/users/{id}/following?&user.fields=name', headers={'Authorization' : f'Bearer {bear}'})

    print(r1.json())
    
    return r1.json()["data"]

    