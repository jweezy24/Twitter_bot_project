import requests
import os
import json
bear = os.environ["BEARER"]

def get_tweet_context(ids):
    string = ''

    for id in ids:
        string += f"{id},"
    string=string[:len(string)-2]
    print(string)
    r = requests.get(f'https://api.twitter.com/2/tweets?ids={string}&tweet.fields=context_annotations', headers={'Authorization' : f'Bearer {bear}'})
    
    if r:
        print(r.json())
    else:
        print(r)